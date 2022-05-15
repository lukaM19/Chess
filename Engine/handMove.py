from cgitb import handler
import enum
from sre_constants import SUCCESS
import cv2
import time
import mediapipe as mp
import pyautogui 
import numpy as np

capture= cv2.VideoCapture(0)
capture.set(3,640)
capture.set(4,480)
mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw=mp.solutions.drawing_utils
prevSmoothX,prevSmoothY=0,0

initialTime=0
currentTime=0

while True:
    success,img=capture.read()
    imgRGB= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results= hands.process(imgRGB)

    
    clicked=False
    if results.multi_hand_landmarks:
        for handLandmark in results.multi_hand_landmarks:
            for id,coordinates in enumerate(handLandmark.landmark):
                h,w,c=img.shape
                if id==8 or id==12 or id==4 or id ==5 or id ==9:
                    xPixelPosition,yPixelPosition=int(coordinates.x*w),int(coordinates.y*h)
                    #print(id,xPixelPosition,yPixelPosition)
                    cv2.circle(img,(xPixelPosition,yPixelPosition),15,(255,0,255),cv2.FILLED)
                    #print(x4,x8,x12)
                    if id== 4:
                        x4,y4=int(coordinates.x*w),int(coordinates.y*h)
                    if id== 8:
                        x8,y8=int(coordinates.x*w),int(coordinates.y*h) 
                    if id == 5:
                        x5,y5= int(coordinates.x*w),int(coordinates.y*h) 
                    if id == 9:
                        x9,y9= int(coordinates.x*w),int(coordinates.y*h) 
                    if id== 12:
                        x12,y12=int(coordinates.x*w),int(coordinates.y*h)
                        if not clicked and (abs(y4-y8)<50 and abs(y4-y12)<50 and abs(y8-y12)<50)and (abs(x4-x8)<50 and abs(x4-x12)<50 and abs(x8-x12)<50):
                            print("CLICK",y4,y8,y12)
                            pyautogui.click()
                            clicked=True
                            print((y5-y8))
                        else:
                            clicked=False
                        if (y9-y12)>40 and (y5-y8)>40 and (abs(x8-x12)<30)  :
                            print("SLIDE")
                            
                            screenRad=25
                            mouseX=np.interp((x8+x12)/2,(screenRad,640-screenRad),(0,pyautogui.size()[0]))
                            mouseY=np.interp((y8+y12)/2,(screenRad,350-screenRad),(0,pyautogui.size()[1]))
                            if clicked:
                                pyautogui.dragTo(mouseX,mouseY)
                            else:
                                pyautogui.moveTo(mouseX,mouseY)
            screenRad=25
            cv2.rectangle(img,(screenRad,screenRad),(640-screenRad,350-screenRad),(0,255,0),2)
            mpDraw.draw_landmarks(img,handLandmark,mpHands.HAND_CONNECTIONS)
    currentTime=time.time()

    fps=1/( currentTime-initialTime)
    initialTime=currentTime
    #cv2.putText(img,str(int(fps)),(10,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    #cv2.imshow("Image",img)
    cv2.waitKey(1)