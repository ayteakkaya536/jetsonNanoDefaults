""" This is the default code to connect to USB camera """

import cv2
print(cv2.__version__)
dispW=320
dispH=240
flip=2
cam=cv2.VideoCapture(1)  # 0, 1, or 2, depends on the port number camera uses. there migth be multiple cameras
#** resize the frame size
# cam.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)

#** save videos --> saving happens within the while loop, please look for "save video", make sure that the path for folder exist
#outVid=cv2.VideoWriter('folderVideo/myCam.avi',cv2.VideoWrite_fourcc(*'XVID'),21,(dispW,dispH)) #21 is frame rate

#** READ from an existing video
#cam=cv2.VideoCapture('folderVideo/myCam.avi')

while True:
    ret, frame = cam.read()
    cv2.imshow('NameWindowPiCam', frame)
    #** placement of the window on the screen **
    #cv2.moveWindow('NameWindowPiCam', 0, 0) #this is t palce the screen at the defined location, otherwise location will be random
    #** changing the color **
    #gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   # this will output gray color of same frames
    #** resizing the images **
    #frameSmall=cv2.resize(frame,(320,240))
    #cv2.imshow('resizedImage',frameSmall)
    #** SAVE VIDEO **
    #outVid.write(frame)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()

#** SAVE VIDEO CLOSE
#outVid.release()
cv2.destroyAllWindows()
