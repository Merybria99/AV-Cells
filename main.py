import csv
import math
from cmath import sqrt
import os

import cv2 as cv

from libraries import connected_components

directory = "/home/mary/PycharmProjects/esercitazione_21_10/images/Training/"
test_directory = "/home/mary/PycharmProjects/esercitazione_21_10/images/Test/"


def get_correct_number_of_cells( dir ):
    total_occurrences = 0
    occurrences = dict()
    for file in os.listdir(dir):

        if (file.endswith(".csv")):

            file_path = dir + file
            with open(file_path, 'r') as file:
                csvreader = csv.reader(file, delimiter=';')
                string = (str(file).split('.csv')[0]).split('/')[-1]

                for row in csvreader:
                    if row[4] == 'cell':
                        total_occurrences = total_occurrences + 1

                occurrences[string] = total_occurrences
                total_occurrences = 0
    return occurrences


def train( kernel_erode_size=3, kernel_dilate_size=3, kernel_size=3, preprocessing_op='erode'):
    found_cells = dict()
    for images in os.listdir(directory):
        # check if the image ends with png
        if (images.endswith(".png")) and '_mask' not in images:

            image_path = directory + images
            string = (str(images).split('.png')[0]).split('/')[-1]
            image = cv.imread(image_path)
            th, new_contours, contours, hierarchy, out = connected_components.connected_component_img(image,
                                                                                                      kernel_erode_size,
                                                                                                      kernel_dilate_size,
                                                                                                      kernel_size,
                                                                                                      preprocessing_op)

            found_cells[string] = len(new_contours)

            # calcolo dell'area
            area = 0
            for new_contour in new_contours:
                area = area + cv.contourArea(new_contour)

            # print(str(area / len(new_contour)) + ' area media')

            # visualizzazione con baricentro
            for contour in new_contours:
                M = cv.moments(contour)
                if M['m00'] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    cv.drawContours(image, [contour], -1, (0, 255, 0), 2)
                    cv.circle(out, (cx, cy), 2, (0, 0, 255), -1)

            cv.imshow('Thresholded', th)
            cv.imshow('Connected components', out)
            cv.waitKey(1)
            cv.destroyAllWindows()

    return found_cells


def test( kernel_erode_size=3, kernel_dilate_size=3, kernel_size=3, preprocessing_op='erode' ):
    found_cells = dict()
    for images in os.listdir(test_directory):
        if (images.endswith(".bmp")) and '_mask' not in images:

            image_path = test_directory + images
            string = (str(images).split('.bmp')[0]).split('/')[-1]
            image = cv.imread(image_path)
            th, new_contours, contours, hierarchy, out = connected_components.connected_component_img(image,
                                                                                                      kernel_erode_size,
                                                                                                      kernel_dilate_size,
                                                                                                      operation_type=preprocessing_op)

            print('cellule trovate: '+ str(len(new_contours)))
            found_cells[string] = len(new_contours)

            # calcolo dell'area
            area = 0
            for new_contour in new_contours:
                area = area + cv.contourArea(new_contour)

            print(str(area / len(new_contour)) + ' area media')

            # visualizzazione con baricentro
            for contour in new_contours:
                M = cv.moments(contour)
                if M['m00'] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    cv.drawContours(image, [contour], -1, (0, 255, 0), 2)
                    cv.circle(out, (cx, cy), 2, (0, 0, 255), -1)

            cv.imshow('Thresholded', th)
            cv.imshow('Connected components', out)
            cv.waitKey(1)
            cv.destroyAllWindows()
    return found_cells


if __name__ == "__main__":
    total_performances = dict()
    performances = dict()
    """
        training part
    
    preprocessing_operations = ['erode', 'erode-dilate', 'dilate', 'open']
    kernel_sizes = [3, 5, 7, 9, 11, 13]

    for op in preprocessing_operations:
        for kernel_size in kernel_sizes:

            cells = train(kernel_erode_size=kernel_size, kernel_dilate_size=kernel_size, kernel_size=kernel_size,
                          preprocessing_op=op)
            expected_cells = get_correct_number_of_cells(directory)
            std_dev = 0
            for key in cells:
                difference = expected_cells[key] - cells[key]
                print(difference)
                performances[key] = difference
                std_dev = std_dev + (difference * difference)
            total_performances[str(op) + '_' + str(kernel_size)] = sqrt(int(std_dev))

    print("statistiche finali")
    min = ''
    min_value = math.inf
    for key in total_performances:
        print('performance : ' + key)
        print(total_performances[key])
        print('\n')
        if total_performances[key].real < min_value:
            min = key
            min_value = total_performances[key].real

    print('best configuration : ' + min)
    """
    """
        test part
    """
    cells = test(kernel_erode_size=13, kernel_dilate_size=13, preprocessing_op='erode-dilate')
    expected_cells = get_correct_number_of_cells(test_directory)
    for key in cells:
        performances[key] = expected_cells[key] - cells[key]
    print(performances)
