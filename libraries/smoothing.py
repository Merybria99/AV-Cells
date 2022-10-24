import os

import cv2
import numpy as np


def average_smooth( img, kernel ):
    smooth_img = cv2.filter2D(img, -1, kernel)
    return smooth_img


def gaussian_smooth( img, kernel_width, kernel_height ):
    smooth_img = cv2.GaussianBlur(img, (kernel_width, kernel_height), 0)
    return smooth_img


def median_smooth( img, kernel_width ):
    smooth_img = cv2.medianBlur(img, kernel_width - 1 if kernel_width % 2 == 0 else kernel_width)
    return smooth_img


def image_smooth( name, kernel_width, kernel_height, smooth_mode ):
    path = str(os.curdir) + '/images/' + name
    img = cv2.imread(path)
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow('img', img)

    modes = {'average':  average_smooth(img, np.ones((kernel_width, kernel_height), np.float32) / (
            kernel_width * kernel_height)),
             'gaussian': gaussian_smooth(img, kernel_width, kernel_height),
             'median':   median_smooth(img, kernel_width)}

    try:
        filtered_img = modes[smooth_mode]
    except:
        print("modo non corretto")
        exit()

    cv2.namedWindow('smooth_img', cv2.WINDOW_NORMAL)
    cv2.imshow('smooth_img', filtered_img)
    k = cv2.waitKey(0)
