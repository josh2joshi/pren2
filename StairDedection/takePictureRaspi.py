import cv2 as cv
from picamera import PiCamera
from picamera.array import PiRGBArray
import time

RESOLUTION = (640, 480)

camera = PiCamera()
camera.resolution = RESOLUTION
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=RESOLUTION)

time.sleep(0.1)
counter = 1
for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
    image = frame.array
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    key = cv.waitKey(1) & 0xFF
    if key == ord(" "):
        cv.imwrite(f'objectDark{counter}.png', image)
        counter = counter + 1

    cv.imshow("Frame", image)
    rawCapture.truncate(0)

# for i in range(6):
#   cam = cv2.VideoCapture(i)
#  if cam is None:
#     img = cam.read()
#    if img is None:
#       print(i)
# else:
#   print(i , " is undefind")
