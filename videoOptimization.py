#  !!!! TESTED WROKING !!!
#copy of  'faceRecognizeKwonFaces.py' to optimize it
### !!! TEST RESULT 5-9 frame per second it doing okay with below size (frame factor 0.25) and code
# XX python version 3.9
# pip --version
# XX pip version 21.0.1
# pip install --upgrade pip
# pip install face-recognition
# pip install opencv-python

import face_recognition
import cv2
import os
import pickle
print (cv2.__version__)
import time

########################
fpsReport=0
scaleFactor=0.25  # will be used to reduce the frame size
# the smaller frame factor, faster the frame pers econd
#!!! the smaller the frame factor, LESS face recognition (whent he face si far or smaller,it will NOT get recognized)
###############


Encodings=[]
Names=[]

with open('train.pkl','rb') as f: #rb stands for raw bit
    Names=pickle.load(f)
    Encodings=pickle.load(f)

font=cv2.FONT_HERSHEY_SIMPLEX
cam=cv2.VideoCapture(0)

timeStamp=time.time()
while True:
    _,frame=cam.read()
    frameSmall=cv2.resize(frame,(0,0),fx=scaleFactor,fy=scaleFactor) #.33 is decrease on size due to slow frame per second processing
    frameRGB=cv2.cvtColor(frameSmall,cv2.COLOR_BGR2RGB)
    facePositions=face_recognition.face_locations(frameRGB,model='cnn')
    allEncodings=face_recognition.face_encodings(frameRGB,facePositions)
    for (top,right,bottom,left), face_encoding in zip(facePositions, allEncodings):
        name='Unknown Person'
        matches=face_recognition.compare_faces(Encodings,face_encoding)
        if True in matches:
            first_match_index=matches.index(True)
            name=Names[first_match_index]
        top=int(top/scaleFactor)
        right=int(right/scaleFactor)
        bottom=int(bottom/scaleFactor)
        left=int(left/scaleFactor)
        cv2.rectangle(frame,(left,top),(right,bottom),(0,0,255),2)
        cv2.putText(frame,name,(left,top-6),font,.75,(0,0,255),2)
    ##################################
    dt=time.time()-timeStamp
    fps=1/dt
    fpsReport=.90*fpsReport + 0.1*fps
    print('fps is = ',round(fpsReport,1))
    timeStamp=time.time()
    cv2.rectangle(frame,(0,0),(100,40),(0,0,255),-1)
    cv2.putText(frame,str(round(fpsReport,1))+' fps',(0,25),font,0.75,(0,255,255,2))
    #############################
    cv2.imshow('Picture',frame)
    cv2.moveWindow('Picture',0,0)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
