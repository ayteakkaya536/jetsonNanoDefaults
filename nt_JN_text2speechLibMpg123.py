## !!!  NOT TESTED !!!  ##
## !! PREFERRED --> work on this to use
## caution !! requires internet access to google, look for alternatives 
## mpg123, gTTS library is needed, run the code on terminal(linux command)
## sudo apt install mpg123
## sudo pip3 install gTTS

import os
from gtts import gTTS
myTest='get ready !'
myOutput=gTTS(text=myText, lang='en', slow=False)
myOutput.save('talk.mp3')
os.system('mpg123 talk.mp3')


