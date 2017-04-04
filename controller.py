#pip install pypiwin32, numpy, opencv-python

import win32api
import win32con

import time
import os


import numpy as np
import cv2

# For windows
def simulateMouseClick(pos):
    win32api.SetCursorPos(pos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def currentMillis():
    return int(round(time.time() * 1000))

# Initialize first webcam with parameters
# sufficient to detect brightness change 
# on an already bright surface, when a laser hits it
cam = cv2.VideoCapture(0)

cam.set(cv2.CAP_PROP_BRIGHTNESS, 10)
cam.set(cv2.CAP_PROP_EXPOSURE, 60)
cam.set(cv2.CAP_PROP_CONTRAST, 40) # 30 -> default
cam.set(cv2.CAP_PROP_GAIN, 25) # 30~40 -> projector/screen, 20~30 -> laser
cam.set(cv2.CAP_PROP_SATURATION, 40)

totalFrames = 0

undetectedLaserFrames = 0

laserInactivityThreshold = 5 #frames
maxValueThreshold = 120 # Brightness for laser

laserPrev = False

# Calibration corners
topLeft = (-1,-1)
botRight = (-1, -1)

def isCalibrated():
    return False

while(True):
    ret, frame = cam.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    h,s,v = cv2.split(hsv)
    (minValue, maxValue, minLoc, maxLoc) = cv2.minMaxLoc(v)

    if(maxValue > maxValueThreshold): # Possible laser at 'maxLoc' 
        if(laserPrev == False and undetectedLaserFrames >= laserInactivityThreshold): # Shot
            if(isCalibrated()): # Calibration is negative edge triggered, so no else
                simulateMouseClick(maxLoc)

        laserPrev = True
        undetectedLaserFrames = 0

    else: # If no laser
        if(laserPrev == True): # Negative edge calibration trigger
            if(not isCalibrated()):
                #Calibrate 

        laserPrev = False
        undetectedLaserFrames += 1

    pointX = -1
    pointY = -1

    
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

            
    # Draw calibration edges        

    if(not (calX == -1 or calY == -1)):
       cv2.circle(frame, (calX, calY), 5, (0,255,0), -1)
    if(not (calW == -1 or calH == -1)):
        cv2.circle(frame, (calX + calW, calY), 5, (0,255,0), -1)
        cv2.circle(frame, (calX + calW, calY + calH), 5, (0,255,0), -1)
        cv2.circle(frame, (calX, calY + calH), 5, (0,255,0), -1)
        
    cv2.imshow('Configured Webcam', frame)
    cv2.imshow('HSV', hsv)
    cv2.imshow('V - Brightness', v)

    totalFrames += 1

    # Till key 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
	    break


# Cleanup
cam.release()
cv2.destroyAllWindows()
