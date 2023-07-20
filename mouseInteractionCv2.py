""" This is the default code to opnCV mouse controls, with usb camera"""

import cv2
print(cv2.__version__)
evt=-1 #will be used in if statement for event 
coord=[]  # array will be used to keep the clicked points on the screen
def click(event,x,y,flags,params):
    global pnt
    global evt
    if event==cv2.EVENT_LBUTTONDOWN: #left click will collect coordinates
        print('Mouse Event was: ', event)
        print(x,',',y)
        coord.append(pnt)  #this array will keep all previously clicked points
        print(coord)
        pnt=(x,y)
        evt=event
    if event==cv2.EVENT_RBUTTONDOWN: #rigth click will collect colorrgb values
        print('Mouse Event was: ', event)
        print(x,',',y)
        blue=frame[y,x,0] #0 is blue comes from BGR (RGB regular colors)
        green=frame[y,x,1]
        red=frame[y,x,2]
        print(blue,green,red)
dispW=320
dispH=240
flip=2
cv2.namedWindow('NameWindow')
cv2.setMouseCallback('NameWindow',click) # this is the liostener for teh mouse events

cam=cv2.VideoCapture(1)  # 0, 1, or 2, depends on the port number camera uses. there migth be multiple cameras


while True:
    ret, frame = cam.read()
    for pnts in coord:
        cv2.circle(frame,pnts,5,(0,0,255),-1) #this will show all teh previously clicked points
        font=cv2.FONT_HERSEY_PLAIN
        myStr=str(pnts)
        cv2.putText(frame,myStr,pnts,font,1.5,(255,0,0),2) # this will put the coordinartes of the dots
    cv2.imshow('NameWindow', frame)
    cv2.moveWindow('NameWindow',0,0)

    keyEvent=cv2.waitKey(1) # 1 is 1 sec to wait for the keypad 
    if keyEvent==ord('q'):
        break
    if keyEvent==ord('c'):
        coord=[]

cam.release()
cv2.destroyAllWindows()
