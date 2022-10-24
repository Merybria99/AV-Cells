import os
from random import randint

import cv2 as cv
import numpy as np
from libraries import morphology


def get_circular_kernel( diameter ):
    mid = (diameter - 1) / 2
    distances = np.indices((diameter, diameter)) - np.array([mid, mid])[:, None, None]
    kernel = ((np.linalg.norm(distances, axis=0) - mid) <= 0).astype(int)

    return kernel


def connected_component( name ):
    path = str(os.curdir) + '/images/' + name
    img = cv.imread(path)

    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    cv.namedWindow('img', cv.WINDOW_NORMAL)
    cv.imshow('img', img)

    try:
        connected_c_img = cv.connectedComponents(img)
    except:
        exit()

    k = cv.waitKey(0)


def erode_dilate( image, kernel_erode_size=3, kernel_dilate_size=3 ):
    kernel_erode = np.ones((kernel_erode_size, kernel_erode_size), np.uint8)
    kernel_dilate = np.ones((kernel_dilate_size, kernel_dilate_size), np.uint8)
    er = cv.erode(image, kernel_erode, 1)
    return cv.dilate(er, kernel_dilate, 1)


def connected_component_img( img, kernel_erode_size, kernel_dilate_size, kernel_size=3, operation_type='erode' ):
    b, g, r = cv.split(img)
    ret3, th = cv.threshold(g, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    w, h = th.shape

    operations = {'erode':        cv.erode(th, np.ones((kernel_erode_size, kernel_erode_size), np.uint8), 1),
                  'open':         cv.morphologyEx(th, cv.MORPH_OPEN, np.ones((kernel_size, kernel_size), np.uint8),
                                                  iterations=1),
                  'erode-dilate': erode_dilate(th, kernel_erode_size, kernel_dilate_size),
                  'dilate': cv.dilate(th, np.ones((kernel_dilate_size, kernel_dilate_size), np.uint8), 1)}

    result = operations[operation_type]

    contours, hierarchy = cv.findContours(result, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)

    out = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    new_contours = list()
    for c in contours:
        x = list()
        y = list()
        for c_i in c:
            for el in c_i:
                x.append(el[1])
                y.append(el[0])

        if not (0 in x or 0 in y or w - 1 in x or h - 1 in y):
            cv.drawContours(out, [c], 0, (randint(50, 255), randint(50, 255), randint(50, 255)), thickness=cv.FILLED)
            new_contours.append(c)

    return th, new_contours, contours, hierarchy, out
