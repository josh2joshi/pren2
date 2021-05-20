import sys
import cv2 as cv
import numpy as np
import math as math

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




def main(argv):
    MINLINELENGTH = 100
    MAXHORIZONTALTILT = 5


    default_file = 'Pictures/andrew/signal-2021-03-04-090319_008.jpeg'
    filename = argv[0] if len(argv) > 0 else default_file

    src = cv.imread(filename, cv.IMREAD_GRAYSCALE)

    if src is None:
        print ('Error opening image!')
        print ('Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
        return -1

    # get Coutour of Pictures
    dst = cv.Canny(src, 50, 200, None, 3)

    # Copy edges to the images that will display the results in BGR
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)

    # Get all streight lines in Pictures
    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)
    inputImage = np.zeros((src.shape[0], src.shape[1], 3), np.uint8)
    outputImage = np.zeros((src.shape[0], src.shape[1], 3), np.uint8)

    height = src.shape[0]

    lines = []
    sortedByGradient = []



    #Loop through all lines an calc degrees and offset
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            #    (l[1] >= l[3] and l[1] <= l[3] + 10) horizontal Lines
            line = Line(l[0], l[1], l[2], l[3])
            cv.line(cdst, (l[0], l[1]), (l[2], l[3]), (0, 255, 0), 1, cv.LINE_AA)
            if (line.degree < 11 and line.degree > -11) and line.offset >= 0:
                lines.append(line)
                print(line.degree)
                cv.line(inputImage, (line.x1, line.y1), (line.x2, line.y2), (0, 0, 255), 1, cv.LINE_AA)



    DEGREEBUCKET = 1
    OFFSETBUCKET = 10
    newLines = []
    lines.sort(key=lambda x: x.degree)
    angle = lines[0].degree
    tempLines = []
    for line in lines:
        # print(count)
        if (line.degree - angle) > DEGREEBUCKET and len(tempLines) > 0:
            # print(len(tempLines))
            tempOffsetList = []
            tempLines.sort(key=lambda x: x.offset)
            offset = tempLines[0].offset
            for tempLine in tempLines:
                # print(tempLines[i + 1].offset - offset)
                if (tempLine.offset - offset) > OFFSETBUCKET:
                    tempOffsetList.sort(key=lambda x: x.x1)
                    if len(tempOffsetList) > 1:
                        newLines.append(Line(tempOffsetList[0].x1, tempOffsetList[0].y1, tempOffsetList[len(tempOffsetList) - 1].x2, tempOffsetList[len(tempOffsetList) - 1].y2))
                    # else:
                    #     newLines.append(Line(tempOffsetList[0].x1, tempOffsetList[0].y1,tempOffsetList[0].x2, tempOffsetList[0].y2))
                    tempOffsetList.clear()
                    offset = tempLine.offset

                tempOffsetList.append(tempLine)
            tempLines.clear()
            angle = line.degree
        tempLines.append(line)


    print(len(newLines))
    for newLine in newLines:
        cv.line(outputImage, (newLine.x1, newLine.y1), (newLine.x2, newLine.y2), (255, 0, 0), 1, cv.LINE_AA)
    # Show results
    # cv.imshow("Source", src)
    cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdst)
    cv.imwrite("DetectedLines.jpeg", cdst)
    # cv.imshow("Detected Lines (in ansform", src)
    cv.imshow("inputImage", inputImage)
    cv.imshow("outputImage", outputImage)
    cv.imwrite("inputImage.jpeg", inputImage)
    cv.imwrite("outputImage.jpeg", outputImage)
    # cv.imwrite("foo.jpeg",cdstP)


    # Wait and Exit
    cv.waitKey()
    return 0
    ## [exit]

if __name__ == "__main__":
    main(sys.argv[1:])