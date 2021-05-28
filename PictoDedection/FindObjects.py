import numpy as np
import cv2 as cv

from FindObject import findObject


def findObjects(img, minimumsize, whratio, threshold, filtersize, padding, maximumnumber):
    h = np.ones(filtersize) / np.prod(filtersize)
    img = cv.filter2D(img, -1, h, borderType=cv.BORDER_DEFAULT)

    objectDetected = []


    i = 0
    while np.amin(img) < threshold and (i <= maximumnumber):
        xmin, ymin, xmax, ymax = findObject(img, threshold, filtersize, padding)
        yMinSize = ymax - ymin + 1
        xMinSize = xmax - xmin + 1


        if yMinSize >= minimumsize[0] and xMinSize >= minimumsize[1] and \
                (max(yMinSize / xMinSize, xMinSize / yMinSize) < whratio):
            objectDetected.append((xmin, ymin, xmax, ymax))
            i = i + 1
        img[ymin:ymax, xmin:xmax] = 1.0

    return objectDetected
