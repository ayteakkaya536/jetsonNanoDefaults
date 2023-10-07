# python --version
# XX python version 3.9
# pip --version
# XX pip version 21.0.1
# pip install --upgrade pip
# pip install face-recognition
# pip install opencv-python

## TESTED on Windows OS
## THIS TRAIN the face pictures from known folder AND SAVE as train.pkl

import face_recognition
import cv2
import os
import pickle
import time
print(cv2.__version__)

Encodings=[]
Names=[]
j=0

image_dir='C:\\Users\\aytea\\Intellij_OpenCV\\JetsonNano\\venv\\known'
for root, dirs, files in os.walk(image_dir):
    print(files)
    for file in files:
        path=os.path.join(root,file)
        print(path)
        name=os.path.splitext(file)[0]
        print(name)
        person=face_recognition.load_image_file(path)
        encoding=face_recognition.face_encodings(person)[0]
        Encodings.append(encoding)
        Names.append(name)
print(Names)

## SAVE the trained data
with open('train.pkl','wb') as f:
    pickle.dump(Names,f)
    pickle.dump(Encodings,f)

