### TESTED WORKING on Jetson NANO ####

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


import face_recognition
import cv2
import os
import pickle
import time
print(cv2.__version__)

# fpsReport=0
scaleFactor=0.3

Encodings=[]
Names=[]

with open('train.pkl','rb') as f:
    Names=pickle.load(f)
    Encodings=pickle.load(f)
font=cv2.FONT_HERSHEY_SIMPLEX


cam= cv2.VideoCapture(0) # 0 for built in camera, if USB change it to 1

#FPS COUNT
timeMark=time.time()
fpsFilter=0

while True:

    _,frame=cam.read()
    frameSmall=cv2.resize(frame,(0,0),fx=scaleFactor,fy=scaleFactor)
    frameRGB=cv2.cvtColor(frameSmall,cv2.COLOR_BGR2RGB)
    facePositions=face_recognition.face_locations(frameRGB,model='cnn')
    allEncodings=face_recognition.face_encodings(frameRGB,facePositions)
    for (top,right,bottom,left),face_encoding in zip(facePositions,allEncodings):
        name='Unkown Person'
        matches=face_recognition.compare_faces(Encodings,face_encoding)
        if True in matches:
            first_match_index=matches.index(True)
            name=Names[first_match_index]
        top=int(top/scaleFactor)
        right=int(right/scaleFactor)
        bottom=int(bottom/scaleFactor)
        left=int(left/scaleFactor)
        cv2.rectangle(frame,(left,top),(right, bottom),(0,0,255),2)
        cv2.putText(frame,name,(left,top-6),font,.75,(0,0,255),2)
    # FPS TIME CALCUALATION
    dt=time.time()-timeMark
    timeMark=time.time()
    fps=1/dt
    fpsFilter=.95*fpsFilter + .05 *fps
    cv2.rectangle(frame,(0,0),(100, 40),(0,0,255),-1)
    cv2.putText(frame, str(round(fpsFilter,1))+ 'fps',(0,25),font,.75,(0,255,255,2))
    cv2.imshow('Picture',frame)
    cv2.moveWindow('Picture',0,0)
    if cv2.waitKey(1)==ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
