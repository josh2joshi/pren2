import sys
import cv2 as cv
import numpy as np


def main(argv):
    MINLINELENGTH = 100
    MAXHORIZONTALTILT = 5


    default_file = 'Pictures/stair2.jpeg'
    filename = argv[0] if len(argv) > 0 else default_file

    frame = cv.imread(cv.samples.findFile(filename))

    if frame is None:
        print ('Error opening image!')
        print ('Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
        return -1

    # dst = cv.Canny(src, 50, 200, None, 3)

    # Copy edges to the images that will display the results in BGR
    blurred_frame = cv.GaussianBlur(frame, (5, 5), 0)
    hsv = cv.cvtColor(blurred_frame, cv.COLOR_BGR2HSV)

    lower_gray = np.array([144,0,0])
    upper_grey = np.array([247,255,255])

    mask = cv.inRange(hsv,lower_gray,upper_grey)

    contours, _ = cv.findContours(mask,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)

    for contour in contours:
        area = cv.contourArea(contour)
        cv.drawContours(frame,contour,-1,(0,0,255),3)








    # Show results
    cv.imshow("Source", frame)
    cv.imshow("Mask", mask)
    # cv.imwrite("foo.jpeg",cdstP)


    # Wait and Exit
    cv.waitKey()
    return 0
    ## [exit]

if __name__ == "__main__":
    main(sys.argv[1:])