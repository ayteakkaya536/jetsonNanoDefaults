import time

width=640
height=480

## camera Arduino Pi camera Angle of View: H=62.2 degree, V=48.8 degree, make the calculation of degrees by pixel
## pix per angle
pixPerAngleX = width/62.2
pixPerAngleY = height/48.8
def calculatePixCoordinates(left,top,right,bottom,width,height):
    x = left
    y = top
    w = abs(right - x)
    h = abs(y - bottom)
    objX=x+w/2
    objY=y+h/2
    centerDiffX= (objX - width/2)
    centerDiffY= (objY - height/2)
    return centerDiffX, centerDiffY
## sevo angle calculation
targetAngle =None
prevAngle = None
def smooth(targetAngle, prevAngle):
    #   // *** smoothing ***
    while abs(targetAngle - prevAngle) > 0.1:
        prevAngle = (targetAngle * 0.40) + (prevAngle * 0.60)
        outAngle = round(prevAngle,2)
        #    *** end of smoothing ***
        print(" Target Angle "+str(targetAngle) + " , Current Angle " +str(outAngle))
        # ********* servo angle out command **********
        time.sleep(0.01)

## servo track function
## !! improvement needed, tracking is not ideal, moving is not smooth, also tracking gets out of screen
def servoTrack(left,top,right,bottom,width,height,prevPanAngle,prevTiltAngle):
    # cv2.rectangle(frame,(x,y),(x+w,y-h),(0,255,255),3)
    # (left,top),(right, bottom)
    centerDiffX, centerDiffY = calculatePixCoordinates(left,top,right,bottom,width,height)

    if abs(centerDiffX)>10:
        panAngle=prevPanAngle-centerDiffX/pixPerAngleX
        panAngle=round(panAngle,2)
        smooth(panAngle,prevPanAngle)
        prevPanAngle=panAngle

    if abs(centerDiffY)>10:
        tiltAngle=prevTiltAngle + centerDiffY/pixPerAngleY
        tiltAngle=round(tiltAngle,2)
        smooth(tiltAngle,prevTiltAngle)
        prevTiltAngle=tiltAngle
    return prevPanAngle, prevTiltAngle
servoTrack(100,100,150,200,width,height,45,45)