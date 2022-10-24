import cv2 as cv
import numpy as np
def extract_coloured_pixels(colour):
    ranges={'blue':[[110,50,50],[130,225,225]],'green':[[36,10,10],[70,225,225]],'red':[[0,50,50],[10,225,225]]}
    if colour not in ranges:
        exit(-1)

    cap = cv.VideoCapture(0)
    while(1):
        # Take each frame
        _, frame = cap.read()
        # Convert BGR to HSV
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        # define range of blue color in HSV
        lower = np.array(ranges[colour][0])
        upper = np.array(ranges[colour][1])
        # Threshold the HSV image to get only blue colors
        mask = cv.inRange(hsv, lower,upper)
        # Bitwise-AND mask and original image
        res = cv.bitwise_and(frame,frame, mask= mask)

        cv.imshow('frame',frame)
        cv.imshow('mask',mask)
        cv.imshow('res',res)
        k = cv.waitKey(5) & 0xFF
        if k == 27:
            break
    cv.destroyAllWindows()