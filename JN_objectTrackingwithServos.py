##  NOT TESTED  ################
#################SERVO#####################################
# sudo pip3 install adafruit-circuitpython-servokit 
## must be run with python3, which has adafruit libraries, also openCV, numpy etc.. 
## servos jitters if there is not ENOUGH power (even from power supply). 
## while testing use only one servo at a time, or connect better power supply
import cv2
import numpy as np
import time

from adafruit_servokit import ServoKit

print(cv2.__version__)

def nothing(x):
    pass

cv2.namedWindow('TrackBars')
cv2.moveWindow('TrackBars',1320,0)
cv2.createTrackbar('hueLower', 'TrackBars',96,179,nothing)
cv2.createTrackbar('hueUpper', 'TrackBars',120,179,nothing)
cv2.createTrackbar('satLow', 'TrackBars',160,255,nothing)
cv2.createTrackbar('satHigh', 'TrackBars',255,255,nothing)
cv2.createTrackbar('valLow', 'TrackBars',100,255,nothing)
cv2.createTrackbar('valHigh', 'TrackBars',255,255,nothing)

kit=ServoKit(channels=16)
tilt=45
pan=90

kit.servo[0].angle=pan
kit.servo[1].angle=tilt



#font=cv2.FONT_HERSHEY_SIMPLEX

cam=cv2.VideoCapture(0)
width=cam.get(cv2.CAP_PROP_FRAME_WIDTH)
height=cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
print("width: ", width," height: ", height)



while True:
    _, frame1 = cam.read()

    hsv1=cv2.cvtColor(frame1,cv2.COLOR_BGR2HSV)

    hueLow=cv2.getTrackbarPos('hueLower', 'TrackBars')
    hueUp=cv2.getTrackbarPos('hueUpper', 'TrackBars')

    Ls=cv2.getTrackbarPos('satLow', 'TrackBars')
    Us=cv2.getTrackbarPos('satHigh', 'TrackBars')

    Lv=cv2.getTrackbarPos('valLow', 'TrackBars')
    Uv=cv2.getTrackbarPos('valHigh', 'TrackBars')

    l_b=np.array([hueLow,Ls,Lv])
    u_b=np.array([hueUp,Us,Uv])

    FGmask1=cv2.inRange(hsv1,l_b,u_b)


    cv2.imshow('FGmask1',FGmask1)
    cv2.moveWindow('FGmask1',0,480)

    contours1,_ = cv2.findContours(FGmask1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours1=sorted(contours1,key=lambda x:cv2.contourArea(x),reverse=True)
    for cnt in contours1:
        area=cv2.contourArea(cnt)
        (x,y,w,h)=cv2.boundingRect(cnt)
        if area>=50:
            cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,255),3)
            objX=x+w/2
            objY=y+h/2
            errorPan=objX-width/2
            errorTilt= objY - height/2

            if abs(errorPan)>15:
                pan=pan-errorPan/75

            if abs(errorTilt)>15:
                tilt=tilt-errorTilt/75

            if pan>180:
                pan=180
                print("Pan out of range")
                #print his on the screen not on the terminal
            if pan<0:
                pan=0
                print("Pan out of range")
                #print his on the screen not on the terminal
            if tilt>180:
                tilt=180
                print("Tilt out of range")
                #print his on the screen not on the terminal
            if tilt<0:
                tilt=0
                print("Tilt out of range")
                #print his on the screen not on the terminal
            kit.servo[0].angle=pan
            kit.servo[1].angle=tilt
            break




    cv2.imshow('SafetyCamera',frame1)
    cv2.moveWindow('SafetyCamera',0,0)


    if cv2.waitKey(1)==ord('q'):
        break
cam.release()

cv2.destroyAllWindows()