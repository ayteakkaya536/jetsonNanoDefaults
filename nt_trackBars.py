""" This is the default code to TRACKBARS on to USB camera frame """

import cv2
print(cv2.__version__)
dispW=320
dispH=240
flip=2
def nothing():
    pass

cam=cv2.VideoCapture(1)  # 0, 1, or 2, depends on the port number camera uses. there migth be multiple cameras

# ** naming the window to use it for the track bar
cv2.namedWindow('NameWindow')
#** create teh track bar, both will show on the window wiht the assigned names
cv2.createTrackbar('xVal','NameWindow',0,dispW,nothing)  # xVal is the name of the track bar, 
cv2.createTrackbar('yVal','NameWindow',0,dispH,nothing)

while True:
    ret, frame = cam.read()
    xVal_var=cv2.getTrackbarpos('xVal','NameWindow')
    print(xVal_var)
    yVal_var=cv2.getTrackbarpos('yVal','NameWindow')
    #use the track coordinates on circle
    cv2.circle(frame,(xVal_var,yVal_var),5,(255,0,0),-1)

    cv2.imshow('NameWindow', frame)
    cv2.moveWindow('NameWindow',0,0)

    if cv2.waitKey(1)==ord('q'):
        break
cam.release()

cv2.destroyAllWindows()
