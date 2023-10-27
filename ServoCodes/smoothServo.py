import time

angle =None
prevAngle = None


def smooth(angle,prevAngle):

  
#   angle = angle * 100;        #// multiply by 100
#   prevAngle = prevAngle *100

#   // *** smoothing ***
  while angle != prevAngle:
    angleSmoothed = (angle * 0.10) + (prevAngle * 0.90)
    

    prevAngle = int(angleSmoothed)

    #    *** end of smoothing ***

    print(str(angle) + " , " + str(angleSmoothed) )                  

    time.sleep(0.05)


smooth(10,15)