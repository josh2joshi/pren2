
import cv2 as cv
import numpy as np


FRAME_WIDTH = 1280
FRAME_HEIGHT = 720


# Initialize Webcam

videostream = cv.VideoCapture(0)



ret = videostream.set(3, FRAME_WIDTH)
ret = videostream.set(4, FRAME_HEIGHT)

ranctangles = [[[600, 200],[1200, 400]],
               [[200, 500],[300, 680]],
               [[100, 100],[400, 380]]]
print(ranctangles)


while True:

    ret, frame = videostream.read()

    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) #Black and White

    cvRactangle = []
    for r, p in ranctangles:
        cvRactangle.append(cv.rectangle(frame, (r[0], r[1]), (p[0], p[1]), (0, 0, 255), 3))


    cv.imshow('Objects Detector', frame)

    if cv.waitKey() == ord(' '):
        for r, p in ranctangles:
            cutted = frame[r[1]:p[1],r[0]:p[0]]
            cv.imwrite(f'test_{len(r)}.jpg', cutted)
        # print(height,width)


cv.destroyAllWindows()
print("Done")
