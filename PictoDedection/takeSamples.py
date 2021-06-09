import sys
sys.path.append('/home/pi/newPren')
import cv2 as cv
from picamera import PiCamera
from picamera.array import PiRGBArray
import numpy as np
import time
from adjustBrightness import adjustBrightness
from FindObjects import findObjects


RESOLUTION = (640, 480)
FILTERWINDOWSIZE = (60, 60)
NPIK = 10
PADDING = (6, 6)
SERACH = (6, 6)
THRESHOLD = .35
WHRATIO = 1.5
SMIN = (40, 40)

SCALESIZE = (10, 10)

camera = PiCamera()
camera.resolution = RESOLUTION
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=RESOLUTION)

time.sleep(0.1)
counter = 0
for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
    image = frame.array

    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    image = np.float32(image * 1.0 / 255.0)
    image = adjustBrightness(image, FILTERWINDOWSIZE)

    detectedObjects = findObjects(image, SMIN, WHRATIO, THRESHOLD, SERACH, PADDING, NPIK)
    annInputs = []
    counter = counter + 10
    for i, o in enumerate(detectedObjects):
        cv.rectangle(image, (o[0], o[1]), (o[2], o[3]), (0, 0, 0), 2)
        h = o[3] - o[1] + 1
        w = o[2] - o[0] + 1
        cropImg = image[o[1]:o[1] + h, o[0]:o[0] + w]
        cv.imwrite(f'croppedImmages/object{counter}.png', 255 * cropImg)


    cv.imshow("Frame", image)

    rawCapture.truncate(0)
    key = cv.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv.destroyAllWindows()
print("Done")
