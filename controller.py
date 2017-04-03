#pip install pypiwin32, numpy, opencv-python

import win32api
import win32con

import time
import os


import numpy as np
import cv2

#import model


def simulateMouseClick(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)


def currentMillis():
    return int(round(time.time() * 1000))

def clear():
    os.system('cls')

cam = cv2.VideoCapture(0)

#lowest possible brightness
cam.set(cv2.CAP_PROP_BRIGHTNESS, 10)

cam.set(cv2.CAP_PROP_EXPOSURE, 60)

#default contrast is 30, mess with it after laser
cam.set(cv2.CAP_PROP_CONTRAST, 40)

#with this one you only see lights
#30-40 would be good for projector,
#20-30 for lazer
cam.set(cv2.CAP_PROP_GAIN, 25)

#this may be unnecessary,as well as CAP_PROP_HUE
cam.set(cv2.CAP_PROP_SATURATION, 40)

frames = 0
startTime = currentMillis()

class OutputData:
    fps = 0;
    
    somethingChanged = True

    @staticmethod
    def setFPS(frames):
        if(frames == OutputData.fps):
            return
        OutputData.fps = frames
        OutputData.somethingChanged = True

    @staticmethod
    def print():
        if(not OutputData.somethingChanged):
            return
        print("* =========== *")
        print("FPS: {}".format(OutputData.fps))
        OutputData.somethingChanged = False


undetectedLaserFrames = 0
laserInactivityThreshold = 3 #frames

laserOn = False

calX = -1
calY = -1
calW = -1
calH = -1

# define range of blue color in HSV
lower_color = np.array([110,50,50])
upper_color = np.array([130,255,255])


while(True):

    ret, frame = cam.read()
    frames+=1;

    # Our operations on the frame come here
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    #mask = cv2.inRange(hsv, lower_color, upper_color)
    #res = cv2.bitwise_and(hsv, hsv, mask = mask)
    # Display the resulting frame
    cv2.imshow('Stuff',hsv)

    pointX = -1
    pointY = -1
    laserDetected = False
    
    if(laserDetected):
        if(undetectedLaserFrames > laserInactivityThreshold):
            #State Change: Shot complete
            if(calX == -1 and calY == -1):
                calX = 0
                calY = 0
                continue

            if(calW == -1 and calH == -1):
                calW = 0 - calX
                calH = 0 - calY
                continue

            tarX = (1920 / calW) * (pointX - calX)
            tarY = (1080 / calY) * (pointY - calY)

            #simulateMouseClick(tarX, tarY)
            
            laserOn = False
            

    if(not laserDetected):
        undetectedLaserFrames+=1

    timePassed = currentMillis() - startTime

    if(timePassed > 1000):
        OutputData.setFPS(frames)
        frames = 0
        startTime = currentMillis()

    OutputData.print()

    cv2.circle(frame, (100,100), 5 , (255,255,255), -1)

    if(not (calX == -1 or calY == -1)):
       cv2.circle(frame, (calX, calY), 5, (0,255,0), -1)
    if(not (calW == -1 or calH == -1)):
        cv2.circle(frame, (calX + calW, calY), 5, (0,255,0), -1)
        cv2.circle(frame, (calX + calW, calY + calH), 5, (0,255,0), -1)
        cv2.circle(frame, (calX, calY + calH), 5, (0,255,0), -1)

        
    cv2.imshow('Normal Webcam Feed',frame)

    if cv2.waitKey(1) == ord('q'):
	    break



# When everything done, release the camture
cam.release()
cv2.destroyAllWindows()
