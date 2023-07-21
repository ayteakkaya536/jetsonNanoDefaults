""" This is the default code to ROI with MOUSE CLICKS on to USB camera frame """

import cv2
print(cv2.__version__)
dispW=320
dispH=240
flip=2
# set up mouse click listeners
goFlag=0
def mouse_click(event,x,y,flags,params):
    global x1,y1,x2,y2
    global goFlag
    if event==cv2.EVENT_LBUTTONDOWN:
        x1=x
        y1=y
        goFlag=0
    if event==cv2.EVENT_LBUTTONUP:
        x2=x
        y2=y
        goFlag=1
cv2.namedWindow('NameWindow')
cv2.setMouseCallback('NameWindow',mouse_click)


cam=cv2.VideoCapture(1)  # 0, 1, or 2, depends on the port number camera uses. there migth be multiple cameras


while True:
    ret, frame = cam.read()
    cv2.imshow('NameWindow', frame)
    if goFlag==1:
        frame=cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),3)
        roi=frame[y1:y2,x1:x2]
        cv2.imshow('Copy ROI',roi)
        cv2.moveWindow('Copy ROI', 705,0)
    
    cv2.moveWindow('NameWindow',0,0)

    if cv2.waitKey(1)==ord('q'):
        break
cam.release()

cv2.destroyAllWindows()
