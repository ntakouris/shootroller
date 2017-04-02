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

#lowest possible brightness
cam.set(cv2.CAP_PROP_BRIGHTNESS, 0)

cam.set(cv2.CAP_PROP_EXPOSURE, 50)

#default contrast is 30, mess with it after laser
cam.set(cv2.CAP_PROP_CONTRAST, 30)

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
    #cv2.imshow('Webcam Feed',gray)

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
