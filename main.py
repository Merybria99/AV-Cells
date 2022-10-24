import csv
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


def train():
    found_cells = dict()
    for images in os.listdir(directory):
        # check if the image ends with png
        if (images.endswith(".png")) and '_mask' not in images:

            image_path = directory + images
            string = (str(images).split('.png')[0]).split('/')[-1]
            print(string)
            image = cv.imread(image_path)
            th, new_contours, contours, hierarchy, out = connected_components.connected_component_img(image)

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
            cv.waitKey(2000)
            cv.destroyAllWindows()

    return found_cells


def test():
    found_cells = dict()
    for images in os.listdir(test_directory):
        print(images)
        if (images.endswith(".bmp")) and '_mask' not in images:

            image_path = test_directory + images
            string = (str(images).split('.bmp')[0]).split('/')[-1]
            image = cv.imread(image_path)
            th, new_contours, contours, hierarchy, out = connected_components.connected_component_img(image)

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
            cv.waitKey(500)
            cv.destroyAllWindows()
    return found_cells


if __name__ == "__main__":
    total_performances = list()
    performances = dict()
    """
        training part
        cells=training()
        expected_cells = get_correct_number_of_cellules(directory)
        for key in cells:
            performances[key] = expected_cells[key] - cells[key]
        print(performances)
    """

    """
        test part
        cells = test()
        expected_cells = get_correct_number_of_cellules(test_directory)
        for key in cells:
            performances[key] = expected_cells[key] - cells[key]
        print(performances)
    """
