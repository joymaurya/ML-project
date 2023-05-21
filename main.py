#-63.5
#0.00
import numpy as np
import cv2
import mediapipe as mp
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
mphands=mp.solutions.hands
hands=mphands.Hands()
cap=cv2.VideoCapture(0)
drawhand=mp.solutions.drawing_utils
while True:
    success,img=cap.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
    if results.multi_hand_landmarks:
        lmlist=[]
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                lmlist.append([id,cx,cy])
            drawhand.draw_landmarks(img,handLms,mphands.HAND_CONNECTIONS)
        if lmlist:
            x1,y1=lmlist[4][1],lmlist[4][2]
            x2,y2=lmlist[8][1],lmlist[8][2]
            cv2.circle(img,(x1,y1),10,(64,86,35),cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (64, 86, 35), cv2.FILLED)
            cv2.line(img,(x1,y1),(x2,y2),(25,64,86),2)
            length=math.hypot(x1-x2,y1-y2)
            if length<40:
                z1=(x1+x2)//2
                z2=(y1+y2)//2
                cv2.circle(img,(z1,z2),10,(64,86,35),cv2.FILLED)
        volrange=volume.GetVolumeRange()
        volmax=volrange[1]
        volmin=volrange[0]
        vol=np.interp(length,[40,250],[volmin,volmax])
        volume.SetMasterVolumeLevel(vol, None)
        point=np.interp(length,[40,250],[400,150])
        cv2.rectangle(img,(50,150),(85,400),(125,35,63),3)
        cv2.rectangle(img,(50,int(point)),(85,400),(125,35,64),cv2.FILLED)
    cv2.imshow('image',img)
    cv2.waitKey(1)