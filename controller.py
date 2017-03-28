import numpy as np
import cv2

cam = cv2.Videocamture(0)

while(True):
    # camture frame-by-frame
    ret, frame = cam.read()
    
    cv2.imshow('Normal Webcam Feed',frame)

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('Webcam Feed',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the camture
cam.release()
cv2.destroyAllWindows()
