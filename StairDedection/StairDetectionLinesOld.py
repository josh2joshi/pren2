import sys
import cv2 as cv
import numpy as np


def main(argv):
    MINLINELENGTH = 100
    MAXHORIZONTALTILT = 5


    default_file = 'Pictures/stair2.jpeg'
    filename = argv[0] if len(argv) > 0 else default_file

    src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_GRAYSCALE)

    if src is None:
        print ('Error opening image!')
        print ('Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
        return -1

    dst = cv.Canny(src, 50, 200, None, 3)

    # Copy edges to the images that will display the results in BGR
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)



    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)
    # print(linesP)
    lines2d = []
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            #    (l[1] >= l[3] and l[1] <= l[3] + MAXHORIZONTALTILT) horizontal Lines MAXHORIZONTALTILT
            #    (l[0] <= l[2]) and l[2]-l[0] >= 100 lines longer than MINLINELENGTH
            # if(l[1] >= l[3] and l[1] <= l[3] + MAXHORIZONTALTILT) and (l[0] <= l[2]) and l[2]-l[0] >= MINLINELENGTH:
            a = linesP[i][0].tolist()
            lines2d.append(a)
            #     cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 1, cv.LINE_AA)
            if (l[0] + 20 >= l[2] and l[0] <= l[2] + 15):
                cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 1, cv.LINE_AA)

    lines2d.sort(key=lambda x: x[1])
    if lines2d is not None:
        for i in range(0, len(lines2d)):
            print(lines2d[i])




    # Show results
    # cv.imshow("Source", src)
    cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)
    # cv.imwrite("foo.jpeg",cdstP)


    # Wait and Exit
    cv.waitKey()
    return 0
    ## [exit]

if __name__ == "__main__":
    main(sys.argv[1:])