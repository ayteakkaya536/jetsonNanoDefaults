##  TESTED WORKING ################
#################SERVO#####################################
# sudo pip3 install adafruit-circuitpython-servokit 
## must be run with python3, which has adafruit libraries
## servos jitters if there is not ENOUGH power (even from power supply). 
## while testing use only one servo at a time, or connect better power supply

import time
from adafruit_servokit import ServoKit
kit=ServoKit(channels=16)
tilt=30
pan=90
kit.servo[0].angle=pan
kit.servo[1].angle=tilt
# for i in range(30,120):
#     kit.servo[0].angle=i
#     time.sleep(.05)
# for i in range(120,30,-1):
#     kit.servo[0].angle=i
#     time.sleep(.05)
for i in range(30,120):
    kit.servo[1].angle=i
    time.sleep(.05)
for i in range(120,30,-1):
    kit.servo[1].angle=i
    time.sleep(.05)
