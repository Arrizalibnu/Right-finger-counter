import cv2 as cv
import mediapipe as mp
import time
import numpy as np
import ModuleHT as mht

cam = cv.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

pastTime = 0
tipIds = [4, 8, 12, 16, 20]
detector  = mht.HandDetector(detectionCon=0.75)
while True:
    succes, img = cam.read()
    img = detector.findHands(img, draw=False)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = []
        # for thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # for another fingers
        for j in range(1, 5):
            if lmList[tipIds[j]][2] < lmList[tipIds[j]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        # total count fingers 
        totalFingers = np.sum(fingers)
        cv.rectangle(img, (20, 255), (170, 425), (57, 9, 23), cv.FILLED)
        cv.putText(img, f"{totalFingers}", (50, 375), cv.FONT_HERSHEY_SIMPLEX, 4,
                   (0, 164, 255),10)

    currentTime = time.time()
    fps = 1/(currentTime-pastTime)
    pastTime = currentTime
    cv.putText(img, f"Fps: {int(fps)}", (20, 50), cv.FONT_HERSHEY_SIMPLEX, 1,
               (0, 255, 130), 2)


    cv.imshow("Camera", img)
    if cv.waitKey(1) == ord("x"):
        break