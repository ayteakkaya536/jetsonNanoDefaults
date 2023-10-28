import time
from threading import Thread

width = 640
height = 480

## camera Arduino Pi camera Angle of View: H=62.2 degree, V=48.8 degree, make the calculation of degrees by pixel
## pix per angle
pixPerAngleX = width / 62.2
pixPerAngleY = height / 48.8


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


def smooth(targetAngle, prevAngle, name):
    #   // *** smoothing ***
    while abs(targetAngle - prevAngle) > 0.1:
        prevAngle = (targetAngle * 0.40) + (prevAngle * 0.60)
        outAngle = round(prevAngle, 2)
        #    *** end of smoothing ***
        print(name + " Target Angle " + str(targetAngle) + " , Current Angle " + str(outAngle))
        # ********* servo angle out command **********
        time.sleep(0.5)


## servo track function
## !! improvement needed, tracking is not ideal, moving is not smooth, also tracking gets out of screen
def servoTrackPAN(left, top, right, bottom, width, height, prevPanAngle, prevTiltAngle):
    # cv2.rectangle(frame,(x,y),(x+w,y-h),(0,255,255),3)
    # (left,top),(right, bottom)
    centerDiffX, centerDiffY = calculatePixCoordinates(left, top, right, bottom, width, height)
    if abs(centerDiffX) > 10:
        panAngle = prevPanAngle - centerDiffX / pixPerAngleX
        panAngle = round(panAngle, 2)
        threadSmooth=Thread(target=smooth,args=(panAngle, prevPanAngle, 'PAN '))
        threadSmooth.daemon = True
        threadSmooth.start()
        prevPanAngle = panAngle
    return prevPanAngle


def servoTrackTILT(left, top, right, bottom, width, height, prevPanAngle, prevTiltAngle):
    centerDiffX, centerDiffY = calculatePixCoordinates(left, top, right, bottom, width, height)
    if abs(centerDiffY) > 10:
        tiltAngle = prevTiltAngle + centerDiffY / pixPerAngleY
        tiltAngle = round(tiltAngle, 2)
        threadSmooth=Thread(target=smooth,args=(tiltAngle, prevTiltAngle, 'TILT '))
        threadSmooth.daemon = True
        threadSmooth.start()
        prevTiltAngle = tiltAngle
    return prevTiltAngle


# panThread = Thread(target=servoTrackPAN, args=(100, 100, 150, 200, width, height, 45, 45))
# tiltThread = Thread(target=servoTrackTILT,args=(100, 100, 150, 200, width, height, 45, 45))

servoTrackPAN(100,100,150,200,width,height,45,45)
servoTrackTILT(100,100,150,200,width,height,45,45)

# panThread.daemon = True
# tiltThread.daemon = True

## start the threads
# tiltThread.start()
# panThread.start()

while True:
    pass
# servoTrack(100,100,150,200,width,height,45,45)
