import cv2
import os


def image_morphological_transform( img, kernel, iterations, name_transform ):

    transforms = {
        'dilate': cv2.dilate(img, kernel, iterations),
        'erode':  cv2.erode(img, kernel, iterations)
    }

    try:
        morph_img = transforms[name_transform]
    except:
        print("modo non corretto")
        exit()

    return morph_img
