import cv2 as cv


def convertSizeForAnn(input, scalesize):
    cropImg = cv.resize(input, scalesize)
    cropImg = cropImg.reshape((1, scalesize[0] * scalesize[1]))
    return cropImg
