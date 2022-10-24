import os
import cv2

import smoothing


def canny_edge_detection( name, th1, th2 ):
    path = str(os.curdir) + '/images/' + name
    img = cv2.imread(path)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow('img', img)

    try:
        edges = cv2.Canny(img, th1, th2)
    except:
        print("modo non corretto")
        exit()

    cv2.namedWindow('canny edges', cv2.WINDOW_NORMAL)
    cv2.imshow('canny edges', edges)
    k = cv2.waitKey(0)


def edge_detection( name, blurring,sobel_kernel_size, kernel_width=3, kernel_height=3):
    path = str(os.curdir) + '/images/' + name
    img = cv2.imread(path)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow('img', img)

    # applico  il blur che possa essere o a media o gaussiano
    modes = {'gaussian': smoothing.gaussian_smooth(img, kernel_width, kernel_height),
             'median':   smoothing.median_smooth(img, kernel_width)}

    try:
        img_blur = modes[blurring]
    except:
        print("modo non corretto")
        exit()

    # applico l'edge detection per sobel
    # Sobel Edge Detection on the X axis
    sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5)
    # Sobel Edge Detection on the Y axis
    sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5)
    # Combined X and Y Sobel Edge Detection
    sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)

    cv2.namedWindow('sobelx edges', cv2.WINDOW_NORMAL)
    cv2.imshow('sobelx edges', sobelx)
    cv2.namedWindow('sobely edges', cv2.WINDOW_NORMAL)
    cv2.imshow('sobely edges', sobely)
    cv2.namedWindow('sobelxy edges', cv2.WINDOW_NORMAL)
    cv2.imshow('sobelxy edges', sobelxy)
    k = cv2.waitKey(0)