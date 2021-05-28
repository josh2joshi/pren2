import cv2 as cv


for x in range(10):
    cap = cv.VideoCapture(x)
    if cap.isOpened():
        print(x)