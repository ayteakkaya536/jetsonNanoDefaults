""" This is the default code to REGION OF INTEREST on to USB camera frame """

import cv2
print(cv2.__version__)
dispW=320
dispH=240
flip=2


cam=cv2.VideoCapture(1)  # 0, 1, or 2, depends on the port number camera uses. there migth be multiple cameras


while True:
    ret, frame = cam.read()
    #define region of inetrest on the frame
    roi=frame[50:250,200:400] # coordinates are y,x (row, column) instead of x,y
    roi_copy=frame[50:250,200:400].copy  #this will create a copy of roi without chnging the original frame
    cv2.imshow('ROI',roi)
    cv2.imshow('NameWindow', frame)
    cv2.moveWindow('ROI',705,0)
    cv2.moveWindow('NameWindow',0,0)

    if cv2.waitKey(1)==ord('q'):
        break
cam.release()

cv2.destroyAllWindows()
