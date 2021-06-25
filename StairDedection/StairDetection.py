import sys
import cv2 as cv
import numpy as np
import math as math
from picamera import PiCamera
from picamera.array import PiRGBArray


RESOLUTION = (640, 480)
DEGREEBUCKET = 1
OFFSETBUCKET = 10
STAIRLINESCOUNT = 10



class Line:

    def __init__(self,x1,y1,x2,y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.calcDegree()
        self.calcOffset()



    def calcOffset(self):
        if (self.x2 - self.x1) > 0:
            self.offset = self.y1 - self.x1 * (self.y2 - self.y1) / (self.x2 - self.x1)
        else:
            self.offset = -1



    def calcDegree(self):
        if (self.x2 - self.x1) > 0:
            self.degree = math.degrees(np.arctan((self.y2 - self.y1) / (self.x2 - self.x1)))
        else:
            self.degree = 90




camera = PiCamera()
camera.resolution = RESOLUTION
camera.framerate = 16
rawCapture = PiRGBArray(camera, size=RESOLUTION)



for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
    image = frame.array
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    image = cv.GaussianBlur(image, (3, 3), 0)
    sigma = np.std(image)
    mean = np.mean(image)
    lower = int(max(0, (mean - sigma)))
    upper = int(min(255, (mean + sigma)))
    image = cv.Canny(image, lower, upper, None, 3)

    imgColor = cv.cvtColor(image, cv.COLOR_GRAY2BGR)



    linesP = cv.HoughLinesP(image, 1, np.pi / 180, 50, None, 50, 10)

    lines = []
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            line = Line(l[0], l[1], l[2], l[3])
            if (line.degree < 11 and line.degree > -11) and line.offset >= 0:
                lines.append(line)
                # cv.line(image, (line.x1, line.y1), (line.x2, line.y2), (0, 0, 255), 1, cv.LINE_AA)

    newLines = []
    lines.sort(key=lambda x: x.degree)
    if len(lines) > 0:
        angle = lines[0].degree
    tempLines = []

    for line in lines:
        if (line.degree - angle) > DEGREEBUCKET and len(tempLines) > 0:
            tempOffsetList = []
            tempLines.sort(key=lambda x: x.offset)
            offset = tempLines[0].offset
            for tempLine in tempLines:
                if (tempLine.offset - offset) > OFFSETBUCKET:
                    tempOffsetList.sort(key=lambda x: x.x1)
                    if len(tempOffsetList) > 1:
                        newLines.append(Line(tempOffsetList[0].x1, tempOffsetList[0].y1, tempOffsetList[len(tempOffsetList) - 1].x2, tempOffsetList[len(tempOffsetList) - 1].y2))
                    tempOffsetList.clear()
                    offset = tempLine.offset

                tempOffsetList.append(tempLine)
            tempLines.clear()
            angle = line.degree
        tempLines.append(line)

    # print(len(newLines))
    for newLine in newLines:
        cv.line(imgColor, (newLine.x1, newLine.y1), (newLine.x2, newLine.y2), (255, 0, 0), 1, cv.LINE_AA)

    if len(newLines) >= STAIRLINESCOUNT:
        print(len(newLines))
        degrees = []
        for newLine in newLines:
            # print(newLine.degree)
            degrees.append(newLine.degree)
        degreeMedian = np.median(degrees)
        if degreeMedian < 0:
            print("We are Left")
        elif degreeMedian > 0:
            print("We are Right")
    else:
        print("No Stair Dedected!!")
        # print(newLine[0].offset)

    cv.imshow("Frame", imgColor)

    rawCapture.truncate(0)
    key = cv.waitKey(1) & 0xFF
    if key == ord("q"):
        break

print("Done")