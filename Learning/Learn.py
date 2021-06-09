import numpy as np
import os
import cv2 as cv
import matplotlib.pyplot as plt
import pickle
from matplotlib.animation import FuncAnimation
from Ann.Ann import Ann


from Ann.ConvertToAnnInput import convertSizeForAnn
from Ann.annForward import annForward

SCALESIZE = (10, 10)
CLASSES = ['bucket', 'hammer', 'pen', 'ruler', 'taco', 'wrench']
NCLASS = 'nothing'
NUMBEROFNODES = [SCALESIZE[0] * SCALESIZE[1], 10, 10]
NUMBEROFLAYERS = len(NUMBEROFNODES)
DEFAULTPATH = 'Learn'
NRUNS = 50
ALPHA = .8

x = 0
y = []

fig = plt.figure()

n = NUMBEROFNODES + [len(CLASSES)]
a = []
z = []
b = []
w = []
for i, o in enumerate(n):
    a.append(np.zeros((1, o)))

for i, o in enumerate(n[1:len(n)]):
    z.append(np.zeros((1, o)))
    b.append(-np.random.rand(1, o) * n[i] / 2)
    w.append(np.random.rand(n[i], o))

images = []
for i, c in enumerate(CLASSES + [NCLASS]):
    imageFiles = os.listdir(f'{DEFAULTPATH}/{c}')
    classImages = []
    for j, o in enumerate(imageFiles):
        image = cv.imread(f'{DEFAULTPATH}/{c}/{o}')
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        image = np.float32(image * 1.0 / 255.0)
        image = convertSizeForAnn(image, SCALESIZE)
        classImages.append(image)
    images.append(classImages)

changeB = b.copy()
changeW = w.copy()
totalCost = np.zeros((1, NRUNS))
totalCost = totalCost.flatten()
desired = np.zeros((1, len(CLASSES)))
for i, o in enumerate(totalCost):
    for j, c in enumerate(changeB):
        changeB[j] = changeB[j] * 0
        changeW[j] = changeW[j] * 0

    totalTrained = 0

    for k, imageList in enumerate(images):
        desired = desired * 0
        if k < len(CLASSES):
            desired[0][k] = 1.0

        for l, input in enumerate(imageList):
            a[0] = input
            a, z = annForward(a, z, b, w)
            cost = np.sum(np.square(a[len(a) - 1] - desired))
            totalTrained = totalTrained + 1
            totalCost[i] = totalCost[i] + cost

            # BackPropagation
            dcda = 2 * (a[len(a) - 1] - desired)
            for m, foo in enumerate(z):
                index = len(z) - m - 1
                dcdb = dcda * 1 / (4 * np.square(np.cosh(z[index] / 2)))
                changeB[index] = changeB[index] + dcdb
                dcdw = np.multiply(dcdb, a[index].T)
                changeW[index] = changeW[index] + dcdw
                dcda = np.dot(dcdb, w[index].T)

    totalCost[i] = totalCost[i] / totalTrained
    y.append(totalCost[i])

    for n, foo in enumerate(z):
        b[n] = b[n] - ALPHA * totalCost[i] / totalTrained * changeB[n]
        w[n] = w[n] - ALPHA * totalCost[i] / totalTrained * changeW[n]

updated_x = list(range(0, NRUNS))
updated_y = np.array(y).flatten()
plt.plot(updated_x, updated_y)
plt.draw()
x = updated_x
y = updated_y
plt.pause(0.2)
fig.clear()

ann = Ann()

ann.fomalscore = totalCost[NRUNS - 1]
ann.classes = CLASSES
ann.a = a
ann.z = z
ann.b = b
ann.w = w
ann.n = n
ann.nClass = NCLASS

annLocation = open("../Ann/ann.pickle", "wb")
pickle.dump(ann,annLocation)

annLocation.close()
