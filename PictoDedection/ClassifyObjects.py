from Ann.annForward import annForward
import numpy as np


def maxAndIndex(array):
    maxVal = array[0]
    index = 0
    for i, a in enumerate(array):
        if a > maxVal:
            maxVal = a
            index = i
    return maxVal, index


def clasifyObject(ann, input):
    ann.a[0] = input
    a, z = annForward(ann.a, ann.z, ann.b, ann.w)
    newA = np.array(a[len(a) - 1]).flatten()
    maxValue, i = maxAndIndex(newA)
    objectClass = ann.classes[i]
    precent = newA[i]
    precentR = precent / sum(newA)
    return objectClass, round(precent, 2), round(precentR, 2)
