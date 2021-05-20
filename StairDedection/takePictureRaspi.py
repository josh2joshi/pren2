import cv2

cam=cv2.VideoCapture(1)
red,img=cam.read()

cv2.imwrite("camera.jpg",img)
cv2.waitKey(0)


#for i in range(6):
 #   cam = cv2.VideoCapture(i)
  #  if cam is None:
   #     img = cam.read()
    #    if img is None:
     #       print(i)
    #else:
     #   print(i , " is undefind")
