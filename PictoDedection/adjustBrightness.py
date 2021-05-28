import numpy as np
import cv2 as cv


def adjustBrightness(img, windowsize):
    h = np.ones(windowsize) / np.prod(windowsize)
    imgAvg = cv.filter2D(img, -1, h, borderType=cv.BORDER_DEFAULT)
    img = cv.subtract(img, imgAvg) + .5
    return img
