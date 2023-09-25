## !!!  NOT TESTED !!!  ##
## espeak library is needed, run the code on terminal(linux command)
## sudo apt-get install espeak

## OPTION 1 ##
import os
import pyttsx3
engine=pyttsx3.init()
engine.setProperty('rate',150)
engine.setProperty('voice','english+m1') # avialable voices are between m1 to m4 for male, f1 to f4 for female
text='get ready!'
engine.say(text)
engine.runAndWait()

