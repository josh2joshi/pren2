import cv2 as cv
from picamera import PiCamera
from picamera.array import PiRGBArray

RESOLUTION = (640, 480)

camera = PiCamera()
camera.resolution = RESOLUTION
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=RESOLUTION)