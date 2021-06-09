import numpy as np


def annForward(a, z, b, w):
    for i, o in enumerate(z):
        z[i] = np.dot(a[i], w[i]) + b[i]
        a[i + 1] = 1 / (1 + np.exp(-z[i]))
    return a, z
