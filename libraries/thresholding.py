import os

import cv2


def and_camera_captures():
    import cv2 as cv
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    ended = False
    img = [None, None]
    while not ended:
        for i in range(0, 2):
            # Capture frame-by-frame
            ret, frame = cap.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            img_name = "opencv_frame_{}.png".format(i)
            cv2.imwrite(str(os.curdir) + '/images/' + img_name, frame)
            img[i] = cv2.imread(str(os.curdir) + '/images/' + img_name)
            cv.waitKey(1000)

        ended = True
        cap.release()
    res = cv2.bitwise_and(img[0], img[1])
    cv2.imshow('res', res)
    k = cv.waitKey(0)
    cv2.destroyAllWindows()


def image_tresholding( name, thresh, maxvalue, mode ):
    """
    Applica dei cambiamenti alle singole componenti dei vari colori secondo modalità specificate
    :param name:nome file
    :param thresh:soglia
    :param maxvalue:valore massimo da dover sostituire
    :param mode: se binary da 0 a quelli che non superano la soglia, maxvalue se la superano
                se binary_inv da 0 se la soglia è superata, mentre maxvalue se non la supera
                se thresh_trunc da threshold value se il punto supera la soglia, inalterata altrimenti
                se thresh_tozero inalterato se supera la soglia, 0 altrimenti
                se thresh_tozero_inv inalterato se non supera la soglia, 0 se la supera
    :return:
    """
    path = str(os.curdir) + '/images/' + name
    img = cv2.imread(path)
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow('img', img)
    try:
        res, thresh_img = cv2.threshold(img, thresh, maxvalue, mode)
    except:
        print("modalità non corretta")
        exit()

    cv2.namedWindow('thresh_img', cv2.WINDOW_NORMAL)
    cv2.imshow('thresh_img', thresh_img)
    k = cv2.waitKey(0)


def image_adaptive_thresholding( name, maxvalue, mode, modeTH, blocksize, C, blurCoefficient ):
    """
     Applica dei cambiamenti alle singole componenti dei vari colori secondo modalità specificate
    :param name: nome file
    :param maxvalue: valore massimo da dover sostituire
    :param mode: modalità di CALCOLO DEL VALORE DI THRESHOLD
                se cv.ADAPTIVE_THRESH_MEAN_C allora il valore di threshold è pari alla media della neighbourhood del pixel c
                se cv.ADAPTIVE_THRESH_GAUSSIAN_C allora il valore è la somma pesata del nieghbouhood di C. Di solito la
                    forma della gaussiana è specificata ma ppuò esse4re cambiata con setGaussianKernel
    :param modeTH: definisco il tipo di threshold, come sopra.
    :param blocksize: taglia della neighbouhood
    :param C: costante sottratta della thresh calcolata
    :param blurCoefficient: effetto blurring per preprocessing dell'immagine (dispari maggiore di 1, se 1 no effetto)
    :return:
    """

    path = str(os.curdir) + '/images/' + name
    img = cv2.imread(path)
    img = cv2.medianBlur(img, blurCoefficient - 1 if (blurCoefficient % 2 == 0) else blurCoefficient)
    # convertire sempre in b/w
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow('img', img)
    try:
        thresh_img = cv2.adaptiveThreshold(img, maxvalue, mode, modeTH, blocksize, C)
    except:
        print("errore nella modalità")
        exit()
    cv2.namedWindow('thresh_img', cv2.WINDOW_NORMAL)
    cv2.imshow('thresh_img', thresh_img)
    k = cv2.waitKey(0)


def image_otsu_thresholding( name, threshold, maxvalue, mode, gassian_blur, blocksize_gblur, sigma ):

    img = name
    if gassian_blur:
        img = cv2.GaussianBlur(img, (blocksize_gblur, blocksize_gblur), sigma)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow('img', img)
    try:
        res, thresh_img = cv2.threshold(img, threshold, maxvalue, mode + cv2.THRESH_OTSU)
    except:
        print("modalità non corretta")
        exit()

    #cv2.namedWindow('thresh_img', cv2.WINDOW_NORMAL)
    #cv2.imshow('thresh_img', thresh_img)
    #k = cv2.waitKey(2000)
    return thresh_img
