#import libs after install it
import cv2
import time
import mediapipe as mp
import math
import numpy as np
from ctypes import cast ,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities , IAudioEndpointVolume
#now we recognize pc volume
dev = AudioUtilities.GetSpeakers()
I = dev.Activate (IAudioEndpointVolume._iid_, CLSCTX_ALL,None)
vol = cast (I,POINTER(IAudioEndpointVolume))


#maling media pipe ready to draw hand marks
mp_drawing = mp.solutions.drawing_utils
#define our frame shape
wCam , hCam = 1250 , 640

cap =cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pt=0
#use media pipe to recognize hands
mp_hd =mp.solutions.hands
hds=mp_hd.Hands(max_num_hands=1)

while True :

    ret , img = cap.read()
    #convert our video from bgr to rgb to make it ready ror media pipe
    RGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    re=hds.process(RGB)
    #now we print our two tips indes
    if re.multi_hand_landmarks:
        tip1=re.multi_hand_landmarks[0].landmark[8]
        tip2=re.multi_hand_landmarks[0].landmark[4]
        x1=tip1.x
        x2 = tip2.x
        y1 = tip1.y
        y2 = tip2.y
        #calc the distance betwin them
        d=math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        print(d)

        mp_drawing.draw_landmarks(img,re.multi_hand_landmarks[0],mp_hd.HAND_CONNECTIONS)
        cv2.line(img ,(int (x1 * img.shape[1] ),int( y1 * img.shape[0])),(int (x2 * img.shape[1]) ,int( y2 * img.shape[0])),(0,0,255),3)
        X=np.interp(d,[0.023122497812726656 , 0.268578703835206 ],[-64.0 , 0.0])
        vol.SetMasterVolumeLevel(X, None)
    Time=time.time()
    fbs = 1/(Time-pt)
    pt=Time
    cv2.putText( img,f"FBS : {int(fbs)}",(70,70),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,250),3)
    cv2.imshow("oussama", img )
    cv2.waitKey(1)