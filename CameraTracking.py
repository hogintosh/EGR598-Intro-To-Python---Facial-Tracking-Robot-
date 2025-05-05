import cv2 
import numpy as np
import dlib
from math import hypot
import os
assert os.path.exists("/Users/seanvellequette/Desktop/FinalPythonProject/shape_predictor_68_face_landmarks.dat"), "model file not found"
import serial
import time

## Sets up baud rate and communication for a trigger command sent to the ESP32
 
esp32Port = '/dev/cu.wchusbserial110' #change this depending on what your MCU is connected to
baudRate = 115200
ser = serial.Serial(esp32Port, baudRate, timeout=1)
time.sleep(2)

## sets up webcam and loads the face predictor.dat file

cap = cv2.VideoCapture(0) #
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
font = cv2.FONT_HERSHEY_PLAIN # a default font that I chose for this project


## Send Trigger command over UART to ESP32

def sendTrigger():
     print("Sending Trigger Command to ESP32")
     ser.write(b'TRIGGER\n')


## Midpoint formula for facial landmark points with X and Y Coordinates

def midpoint(p1, p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2) # midpoint between two given pixels (note has to be integer as you can't have a 1/2 of a pixel)


## Blinking Ratio for between lines horizontally drawn and vertically drawn across the eye

def blinkingRatio(eyePoints, facialLandmarks):
# Horizontal line processing 
    leftPoint = (facialLandmarks.part(eyePoints[0]).x, facialLandmarks.part(eyePoints[0]).y) # Horizontal left point of eye (ex. 39 in Landmarks.png)
    rightPoint = (facialLandmarks.part(eyePoints[3]).x, facialLandmarks.part(eyePoints[3]).y) # Horizontal right point of eye

## Vertical line processing (example midpoint between 37 and 38 in Landmarks.png)
    centerTop = midpoint(facialLandmarks.part(eyePoints[1]),facialLandmarks.part(eyePoints[2])) # Midpoint between two upper eyelid points
    centerBottom = midpoint(facialLandmarks.part(eyePoints[5]),facialLandmarks.part(eyePoints[4])) # Midpoint between two lower eyelid points

    verLineLength = hypot((centerTop[0] - centerBottom[0]), (centerTop[1]-centerBottom[1])) # length from eyelid to eyelid vertically
    horLineLength = hypot((leftPoint[0]-rightPoint[0]),(leftPoint[1]-rightPoint[1])) # length of eye horizontally 

    ratio = horLineLength/verLineLength # ratio between horizontal line drawn  across the eye and vertical line across the eye. When the number gets bigger then the eye is smaller
    #cv2.line(frame, centerTop, centerBottom, (255,0,0), 2) # draws vertical line across eye
    #cv2.line(frame, leftPoint, rightPoint,   (0,0,255), 2) # draws horizontal line across eye
    return ratio


## Function For getting the Gaze Ratio

def getGazeRatioLR(eyePoints,facialLandmarks):
        eyeRegion = np.array([(landmarks.part(eyePoints[0]).x,landmarks.part(eyePoints[0]).y),
                                  (facialLandmarks.part(eyePoints[1]).x,facialLandmarks.part(eyePoints[1]).y),
                                  (facialLandmarks.part(eyePoints[2]).x,facialLandmarks.part(eyePoints[2]).y),
                                  (facialLandmarks.part(eyePoints[3]).x,facialLandmarks.part(eyePoints[3]).y),
                                  (facialLandmarks.part(eyePoints[4]).x,facialLandmarks.part(eyePoints[4]).y),
                                  (facialLandmarks.part(eyePoints[5]).x,facialLandmarks.part(eyePoints[5]).y)], np.int32)
        #cv2.polylines(frame,[eyeRegion],True,(0,0,255),2) # draws bounding box around eye region

        height, width,_ = frame.shape
        mask = np.zeros((height,width),np.uint8)
        cv2.polylines(mask,[eyeRegion],True, 255,2)
        cv2.fillPoly(mask,[eyeRegion], 255)
        eye = cv2.bitwise_and(gray,gray,mask=mask)

        min_x = np.min(eyeRegion[:,0]) # min x,y values for making the mask layer for the shaded eye region
        min_y = np.min(eyeRegion[:,1])
        max_x = np.max(eyeRegion[:,0]) # max x,y values for making the mask layer for the shaded eye region
        max_y = np.max(eyeRegion[:,1])

        shadeEye = eye[min_y: max_y,min_x: max_x]
        _, thresholdEye = cv2.threshold(shadeEye,80, 255, cv2.THRESH_BINARY)
        height, width = thresholdEye.shape

        leftSideThreshold = thresholdEye[0:height, 0:int(width/2)]
        rightSideThreshold = thresholdEye[0:height,int(width/2):width] 

        leftSideWhite = cv2.countNonZero(leftSideThreshold)
        rightSideWhite = cv2.countNonZero(rightSideThreshold)

        if rightSideWhite==0:
             rightSideWhite=1

        gazeRatio = leftSideWhite/rightSideWhite
        return gazeRatio

## Delay code to prevent spamming over UART
lastTriggerTime = 0
cooldown = 5 #seconds

## MAIN
while True: 
    _, frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) # turning frame gray to help with tracking landmarks

    faces = detector(gray)
    for face in faces:

        landmarks = predictor(gray,face)
        
        ## Blink detection
        leftEyeR = blinkingRatio([36,37,38,39,40,41],landmarks) # calls function to find the blinking ratio (distance from eyelid to eyelid compared to length of eye)
        rightEyeR = blinkingRatio([42,43,44,45,46,47],landmarks)
        
        bothBlinkingR = (leftEyeR+rightEyeR)/2 # computes the blinking ratio of both eyes (so winking does not trigger)

        if bothBlinkingR > 5.5: # blinking ratio should be tweaked depending on how sensitive you want it to be
            cv2.putText(frame, "Blinking",(150,150), font, 10, (0,0,255),4) 

        ## Gaze detection function call
        gazeRatioLeftEye = getGazeRatioLR([36,37,38,39,40,41],landmarks)
        gazeRatioRightEye = getGazeRatioLR([42,43,44,45,46,47],landmarks)
        gazeRatioTotal = (gazeRatioLeftEye+gazeRatioRightEye)/2

        currentTime = time.time() # accounts for time between commands

        if gazeRatioTotal <= 0.7: # you can tweak these values to change these thresholds
             if currentTime - lastTriggerTime > cooldown:
                cv2.putText(frame,"RIGHT",(50,150), font, 2, (0,0,255), 3) # looking right (away)
                sendTrigger() # sends the trigger command to esp32 when the person is looking away
                lastTriggerTime = currentTime # acounts for time between UART commands
        elif 0.7 < gazeRatioTotal <1.8:
             cv2.putText(frame,"CENTER",(50,150), font, 2, (0,0,255), 3) # looking at the center of the screen
        else:
             cv2.putText(frame,"LEFT",(50,150), font, 2, (0,0,255), 3) # looking at the robot or far left of computer monitor

        cv2.putText(frame,str(gazeRatioTotal),(50,200),font,2,(0,0,255),3)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) #increase for debugging
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()