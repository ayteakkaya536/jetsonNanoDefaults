### TESTED WORKS  on Jetson NANO ####

### ubuntu/jetpack 4.3 environment library setup
## details here https://forums.developer.nvidia.com/t/simple-accelerated-face-recognition/142679/19
## install below dependencies
# sudo apt-get install python3-pip
# sudo apt-get install libjpeg-dev
## install dlib libraries and build
# sudo wget http://dlib.net/files/dlib-19.21.tar.bz2
# sudo tar jxvf dlib-19.21.tar.bz2
# sudo cd dlib-19.21/
# sudo mkdir build
# sudo cd build/
# sudo cmake ..
# sudo cmake --build .
# sudo cd ../
# sudo python3 setup.py install
# sudo pip3 install face_recognition
# sudo apt-get update
# sudo reboot

## !!! run with python3 !!!


## THIS DOES NOT TRAIN -- TRAIN THE PICfirst and save as train.pkl
## use the file windowsTrainSaveKnownFaces

## CPU on WIN =  rate  0.1 FPS --> usb camera
## GPU on JETSON =  rate  8 FPS -->usb camera

## !!! improvement needed !!
## camera view is cropped, show smaller. also delay

## TESTED WORKS  ################
#################SERVO#####################################
# sudo pip3 install adafruit-circuitpython-servokit
## must be run with python3, which has adafruit libraries, also openCV, numpy etc..
## servos jitters if there is not ENOUGH power (even from power supply).
## while testing use only one servo at a time, or connect better power supply


### !!! IMPORVEMENT NEEDES !! ###
## code tested without activating the servos, servo get outs of position, postion calculation needs work
## camera servo moves oppostie up/down --> correction needed
## 
## movement of the servos are not smooth


import face_recognition
import cv2
import os
import pickle
import time
import numpy as np
from adafruit_servokit import ServoKit
from threading import Thread

print(cv2.__version__)


## Define functions and variables
def nothing(x):
    pass


scaleFactor = 0.3
Encodings = []
Names = []

## CAMERA SETTINGS
## USB
# cam = cv2.VideoCapture(0)  # 0 for built in camera, if USB change it to 1
## PI CSI Camera
dispW=640
dispH=480
flip=2
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
# camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam=cv2.VideoCapture(camSet)

width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
# FPS COUNT
timeMark = time.time()
fpsFilter = 0

## Load the trained known face database
with open('train.pkl', 'rb') as f:
    Names = pickle.load(f)
    Encodings = pickle.load(f)
font = cv2.FONT_HERSHEY_SIMPLEX

## Servo intial setup
kit = ServoKit(channels=16)
prevTiltAngle = 150  # this creates a problem when tilt is 180-tilt during first servoTrack at face detection
prevPanAngle = 90
kit.servo[0].angle = prevPanAngle
kit.servo[1].angle = prevTiltAngle

## camera Arduino Pi camera Angle of View: H=62.2 degree, V=48.8 degree, make the calculation of degrees by pixel
## pix per angle
pixPerAngleX = width / 62.2
pixPerAngleY = height / 48.8
## TEST for angle calculation
pixPerAngleX_W = dispW / 62.2
pixPerAngleY_H= dispH / 48.8


def calculatePixCoordinates(left, top, right, bottom, width, height):
    x = left
    y = top
    w = abs(right - x)
    h = abs(y - bottom)
    objX = x + w / 2
    objY = y + h / 2
    centerDiffX = (objX - width / 2)
    centerDiffY = (objY - height / 2)
    return centerDiffX, centerDiffY


## sevo angle calculation
targetAngle = None
prevAngle = None


def smooth(targetAngle, prevAngle, servoNumber,servoName):
    #   // *** smoothing ***
    while abs(targetAngle - prevAngle) > 0.1:
        prevAngle = (targetAngle * 0.40) + (prevAngle * 0.60)
        outAngle = round(prevAngle, 2)
        #    *** end of smoothing ***
        print(servoName + " Target Angle " + str(targetAngle) + " , Current Angle " + str(outAngle))
        # ********* servo angle out command **********
        if 1 < outAngle < 179:
            # kit.servo[servoNumber].angle = outAngle
            print(servoName + " moved to -- >")
        else:
            print("Out of servo range, servo stopped")
            if outAngle>179:
                outAngle=179
            if outAngle<1:
                outAngle=1
        time.sleep(0.05)


## servo track function
## !! improvement needed, tracking is not ideal, moving is not smooth, also tracking gets out of screen --> test teh smooth if works or not
## !! servoTrackTilt check if the + sogn works, otherwise convert to - 

def servoTrackPAN(left, top, right, bottom, width, height, prevPanAngle, prevTiltAngle):
    # cv2.rectangle(frame,(x,y),(x+w,y-h),(0,255,255),3)
    # (left,top),(right, bottom)
    centerDiffX, centerDiffY = calculatePixCoordinates(left, top, right, bottom, width, height)
    if abs(centerDiffX) > 10:
        panAngle = prevPanAngle - centerDiffX / pixPerAngleX
        ## TEST for angle calculation
        panAngle_W = prevPanAngle - centerDiffX / pixPerAngleX_W
        print("PAN angle ="+str(panAngle)+" PAN W = " + str(panAngle_W))
        panAngle = round(panAngle, 2)
        threadSmooth=Thread(target=smooth,args=(panAngle, prevPanAngle,0, 'PAN '))
        threadSmooth.daemon = True
        threadSmooth.start()
        prevPanAngle = panAngle
    return prevPanAngle


def servoTrackTILT(left, top, right, bottom, width, height, prevPanAngle, prevTiltAngle):
    centerDiffX, centerDiffY = calculatePixCoordinates(left, top, right, bottom, width, height)
    if abs(centerDiffY) > 10:
        tiltAngle = prevTiltAngle + centerDiffY / pixPerAngleY
        ## TEST for angle calculation
        tiltAngle_H= prevTiltAngle + centerDiffY / pixPerAngleY_H
        print("TILT angle ="+str(tiltAngle)+" TILT W = " + str(tiltAngle_H))


        tiltAngle = round(tiltAngle, 2)
        threadSmooth=Thread(target=smooth,args=(tiltAngle, prevTiltAngle,1, 'TILT '))
        threadSmooth.daemon = True
        threadSmooth.start()
        prevTiltAngle = tiltAngle
    return prevTiltAngle
##testig for and error
_, frame = cam.read()
time.sleep(10)
print(' about to get into while loop')

while True:
    # try:
    _, frame = cam.read()
    
    frameSmall = cv2.resize(frame, (0, 0), fx=scaleFactor, fy=scaleFactor)
    frameRGB = cv2.cvtColor(frameSmall, cv2.COLOR_BGR2RGB)
    facePositions = face_recognition.face_locations(frameRGB, model='cnn')
    allEncodings = face_recognition.face_encodings(frameRGB, facePositions)
    for (top, right, bottom, left), face_encoding in zip(facePositions, allEncodings):
        name = 'Unkown Person'
        matches = face_recognition.compare_faces(Encodings, face_encoding)
        if True in matches:
            first_match_index = matches.index(True)
            name = Names[first_match_index]
        top = int(top / scaleFactor)
        right = int(right / scaleFactor)
        bottom = int(bottom / scaleFactor)
        left = int(left / scaleFactor)
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left, top - 6), font, .75, (0, 0, 255), 2)
        if name == 'Unkown Person':
            prevPanAngle = servoTrackPAN(left, top, right, bottom, width, height, prevPanAngle, prevTiltAngle)
            prevTiltAngle = servoTrackTILT(left, top, right, bottom, width, height, prevPanAngle, prevTiltAngle)

    # FPS TIME CALCUALATION
    dt = time.time() - timeMark
    timeMark = time.time()
    fps = 1 / dt
    fpsFilter = .95 * fpsFilter + .05 * fps

    # fps value tag
    cv2.rectangle(frame, (0, 0), (100, 40), (0, 0, 255), -1)
    cv2.putText(frame, str(round(fpsFilter, 1)) + 'fps', (0, 25), font, .75, (0, 255, 255, 2))
    cv2.imshow('Picture', frame)
    cv2.moveWindow('Picture', 0, 0)
    # except:
    #     print('working in while loop, or somehting wrong')
    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
