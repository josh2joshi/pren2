import sys

import initCamera
import numpy as np
import time
from .adjustBrightness import adjustBrightness
import pickle
from Ann.Ann import Ann
from Ann.ConvertToAnnInput import convertSizeForAnn
import cv2 as cv

from .FindObjects import findObjects
from .ClassifyObjects import clasifyObject

# from Ann.ConvertToAnnInput import convertSizeForAnn

annLocation = open("Ann/ann.pickle", "rb")
ann = pickle.load(annLocation)
annLocation.close()

FILTERWINDOWSIZE = (60, 60)
NPIK = 10
PADDING = (6, 6)
SERACH = (6, 6)
THRESHOLD = .35
WHRATIO = 1.5
SMIN = (40, 40)

THRESHOLDOBJECTR = 80
THRESHOLDOBJECT = 90

SCALESIZE = (8, 8)

time.sleep(0.1)
counter = 0
j = 0


def pictoDedection():
    pictogramm = ""
    global j
    j = j + 1
    initCamera.camera.capture(initCamera.rawCapture, format="rgb")
    image = initCamera.rawCapture.array

    image = initCamera.cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    image = np.float32(image * 1.0 / 255.0)
    image = adjustBrightness(image, FILTERWINDOWSIZE)

    detectedObjects = findObjects(image, SMIN, WHRATIO, THRESHOLD, SERACH, PADDING, NPIK)

    annInputs = []
    for i, o in enumerate(detectedObjects):
        h = o[3] - o[1] + 1
        w = o[2] - o[0] + 1
        cropImg = image[o[1]:o[1] + h, o[0]:o[0] + w]
        annInputs.append(convertSizeForAnn(cropImg, SCALESIZE))

    classNames = []
    for i, input in enumerate(annInputs):
        objectClass, precent, precentR = clasifyObject(ann, input)
        classNames.append((objectClass, precent * 100, precentR * 100))

    for object in classNames:
        if object[1] >= THRESHOLDOBJECT and object[2] >= THRESHOLDOBJECTR:
            pictogramm = object[0]

    return 0  # pictogramm
