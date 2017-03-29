import time
import os


import numpy as np
import cv2

#import model

def currentMillis():
    return int(round(time.time() * 1000))

def clear():
    os.system('cls')

cam = cv2.VideoCapture(0)

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
laserInactivityThreshold = 3

laserOn = False
laserDetected = False


while(True):

    ret, frame = cam.read()
    frames+=1;
	
    cv2.imshow('Normal Webcam Feed',frame)

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('Webcam Feed',gray)

    if(laserDetected):
        undetectedLaserFrames+=1
        if(undetectedLaserFrames > laserInactivityThreshold):
            #State Change: Shot complete
            laserOn = False

    timePassed = currentMillis() - startTime

    if(timePassed > 1000):
        OutputData.setFPS(frames)
        frames = 0
        startTime = currentMillis()

    OutputData.print()
    

    if cv2.waitKey(1) == ord('q'):
	    break



# When everything done, release the camture
cam.release()
cv2.destroyAllWindows()
