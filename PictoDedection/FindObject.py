import numpy as np


def minWithIndex(img):
    if len(img) > 0 and len(img[0]):
        minVal = img[0][0]
        index = (0, 0)
        for i, a in enumerate(img):
            for j, b in enumerate(a):
                if b < minVal:
                    minVal = b
                    index = (i, j)
        return (minVal, index)
    else:
        return 0, (0, 0)


def minAndIndex(array):
    minVal = array[0]
    index = 0
    for i, a in enumerate(array):
        if a < minVal:
            minVal = a
            index = i
    return minVal, index


def findObject(img, threshold, filtersize, padding):
    value, index = minWithIndex(img)

    imgXMax = len(img[0])
    imgYMax = len(img)

    dx = int(round(filtersize[1] / 2, 0))
    dy = int(round(filtersize[0] / 2, 0))
    xmin = int(index[1] - dx)
    xmax = int(index[1] + dx)
    ymin = int(index[0] - dy)
    ymax = int(index[0] + dy)

    m = 0.0
    while m < threshold:
        if (xmin < 0):
            xmin = 0
        if (xmax > imgXMax):
            xmax = imgXMax
        if (ymin < 0):
            ymin = 0
        if (ymax > imgYMax):
            ymax = imgYMax

        # print(img[(ymin - 1):(ymax + 2), (xmin - 1):(xmax + 2)])
        # print(minWithIndex(img[(ymin - 1):(ymax + 2), (xmin - 1):(xmax + 2)]))

        if xmin > 0:
            minLeft, i_left = minAndIndex(img[ymin:ymax + 1, xmin - 1])
        else:
            minLeft = 1

        if xmax < imgXMax -1:
            minRight, i_right = minAndIndex(img[ymin:ymax + 1, xmax + 1])
        else:
            minRight = 1

        if ymin > 0:
            minTop, i_top = minAndIndex(img[ymin - 1, xmin:xmax + 1])
        else:
            minTop = 1
        if ymax < imgYMax -1:
            minBottom, i_bottom = minAndIndex(img[ymax + 1, xmin:xmax + 1])
        else:
            minBottom = 1

        m, nindex = minAndIndex([minLeft, minRight, minTop, minBottom])

        if m < threshold:
            if nindex == 0:
                xmin = xmin - dx
                if i_left < dy:
                    ymin = ymin + i_left - dy
                if (i_left > (ymax - ymin - dy)):
                    ymax = ymin + i_left + dy
            elif nindex == 1:
                xmax = xmax + dx
                if (i_right < dy):
                    ymin = ymin + i_right - dy
                if (i_right > (ymax - ymin - dy)):
                    ymax = ymin + i_right + dy
            elif nindex == 2:
                ymin = ymin - dy
                if (i_top < dx):
                    xmin = xmin + i_top - dx
                if (i_top > (xmax - xmin - dx)):
                    xmax = xmin + i_top + dx
            elif nindex == 3:
                ymax = ymax + dy
                if (i_bottom < dx):
                    xmin = xmin + i_bottom - dx
                if (i_bottom > (xmax - xmin - dx)):
                    xmax = xmin + i_bottom + dx

    xmin = xmin - padding[1]
    xmax = xmax + padding[1]
    ymin = ymin - padding[0]
    ymax = ymax + padding[0]
    if (xmin < 0):
        xmin = 0
    if (xmax > imgXMax):
        xmax = imgXMax
    if (ymin < 0):
        ymin = 0
    if (ymax > imgYMax):
        ymax = imgYMax

    return xmin, ymin, xmax, ymax
