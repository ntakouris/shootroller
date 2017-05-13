#pip install pypiwin32, numpy, opencv-python

import win32api
import win32con

import time
import os


import numpy as np
import cv2

# For windows
def simulateMouseClick(pos):
    #Cursor position is integer (current pixel)
    intPos = (int(pos[0]), int(pos[1]))
    win32api.SetCursorPos(intPos)
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
maxValueThreshold = 140 # Brightness for laser

# On the PC
screenWidth = 1920
screenHeight = 1080

# Debug calibration circles color 
calibrationColor = (0, 255, 0)

maxLocPrev = (-1,-1)
laserPrev = False

# Calibration corners
topLeft = (-1,-1)
botRight = (-1, -1)

def isTopCalibrated():
    return topLeft[0] != -1 and topLeft[1] != -1

def isBotCalibrated():
    return botRight[0] != -1 and botRight[1] != -1

def isCalibrated():
    return isTopCalibrated() and isBotCalibrated()

def isPrevMaxLocValid():
    return maxLocPrev[0] != -1 and maxLocPrev[1] != -1 

def getCalibratedWidth():
    return botRight[0] - topLeft[0]

def getCalibratedHeight():
    return botRight[1] - topLeft[1]

while(True):
    ret, frame = cam.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # find the colors within the specified boundaries and apply mask
    mask = cv2.inRange(hsv, np.array([102,70,36]), np.array([143,255,255])) #we only want purple
    hsv = cv2.bitwise_and(hsv, hsv, mask = mask)
    
    h,s,v = cv2.split(hsv)
    (minValue, maxValue, minLoc, maxLoc) = cv2.minMaxLoc(v)

    #print("Undetected laser frames: {}".format(undetectedLaserFrames))

    if(maxValue > maxValueThreshold): # Possible laser at 'maxLoc'
        #print("Possible laser at maxLoc")
        if(laserPrev == False): #and undetectedLaserFrames >= laserInactivityThreshold): # Shot
            print("Laser -> ON")
            laserPrev = True
            if(isCalibrated()): # Calibration is negative edge triggered, so no else
                locX = (screenWidth / getCalibratedWidth() ) * (maxLoc[0] - topLeft[0])
                locY = (screenHeight / getCalibratedHeight() ) * (maxLoc[1] - topLeft[1])
                simulateMouseClick((locX, locY))
        
        #undetectedLaserFrames = 0
    else: # If no laser
        if(laserPrev == True): # Negative edge calibration trigger
            print("Laser -> OFF")
            if(not isCalibrated()):
                print("Not fully calibrated,")
                if(not isPrevMaxLocValid()):
                    print("Can't calibrate, prevMaxLoc is not valid")
                    continue # ?
                else: # Calibrate
                    if(not isTopCalibrated()):
                        print("Calibrating Top Left Corner")
                        topLeft = maxLocPrev
                    elif(not isBotCalibrated()):
                        print("Calibrating Bot Left Corner")
                        botRight = maxLocPrev

        laserPrev = False
        #undetectedLaserFrames += 1

    if(laserPrev == True):
        maxLocPrev = maxLoc
       
    # Draw calibration edges on actual webcam
    if(isTopCalibrated()):
        cv2.circle(frame, topLeft, 5 , calibrationColor, -1)
    if(isBotCalibrated()): # Top would be already calibrated
        cv2.circle(frame, botRight, 5, (0,255,0), -1)
        cv2.circle(frame, (topLeft[0] + getCalibratedWidth() , topLeft[1]), 5, calibrationColor, -1) # Top Right 
        cv2.circle(frame, (topLeft[0], botRight[1]), 5, calibrationColor, -1) # Bot Left
        
    cv2.imshow('Configured Webcam', frame)
    #cv2.imshow('HSV', hsv) # Masked HSV won't show a proper image
    cv2.imshow('V - Brightness', v) # Useful but will ditch in future

    totalFrames += 1

    # Till key 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
	    break


# Cleanup
cam.release()
cv2.destroyAllWindows()
