""" This is the default code to DRAW SHAPES on to USB camera frame """

import cv2
print(cv2.__version__)
dispW=320
dispH=240
flip=2
cam=cv2.VideoCapture(1)  # 0, 1, or 2, depends on the port number camera uses. there migth be multiple cameras
#** resize the frame size
# cam.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)
#** get the frame size in case with is not set initially**
#dispW= int(cam.get(cv2.CAP_PROP_FRAME_WIDTH, dispW))

while True:
    ret, frame = cam.read()
    #** DRAW SHAPES **
    #frame=cv2.rectangle(frame,(first corner coordinates),(second corner),(BGR brigtness),line thicnkness)
    frame=cv2.rectangle(frame,(140,100),(180,140),(255,0,0),4)
    frame=cv2.circle(frame,(140,100),(180,140),(255,0,0),-1) # -1 will make the shape solid
    frame=cv2.line(frame,(10,10),(180,140),(255,0,0),4)
    frame=cv2.arrowedLine(frame,(0,0),(180,140),(255,0,0),4)
    fnt=cv2.FONT_HERSEY_DUPLEX
    frame=cv2.putText(frame, 'my first text', (300,300),fnt,1,(255,0,255),2) # 1 is size, 2 is thicnkess, can be changed

    cv2.imshow('NameWindowPiCam', frame)

    if cv2.waitKey(1)==ord('q'):
        break
cam.release()

cv2.destroyAllWindows()
