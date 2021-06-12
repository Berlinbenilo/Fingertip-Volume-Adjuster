import cv2
import time
import numpy as np
import handtrackingmodule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, HCam = 640,480

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,wCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.75)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()

vol=0
volbar=400
volper = 0

minVol = volRange[0]
maxvol = volRange[1]


while True:
    Success,img = cap.read()
    img = detector.findhands(img,draw=False)
    lmlist = detector.findposition(img,draw=False)
    if len(lmlist) !=0:
        # print(lmlist[4],lmlist[8])
        x1,y1 = lmlist[4][1],lmlist[4][2]
        x2,y2 = lmlist[8][1],lmlist[8][2]
        cx,cy = (x1+x2)//2,(y1+y2)//2

        cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)

        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),1)
        cv2.circle(img, (cx,cy), 10, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1,y2-y1)
        # print(length)

        if length<20:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
        # hand range 20  -  200
        # volume range -63.5 to 0
        vol = np.interp(length,[20,170],[minVol,maxvol])
        volbar = np.interp(length,[20,170],[400,150])
        volper = np.interp(length, [20, 170], [0,100])
        print(length,vol)
        volume.SetMasterVolumeLevel(vol, None)

    cv2.rectangle(img,(50,150),(70,400),(255,0,0),2)
    cv2.rectangle(img, (50,int(volbar)), (70, 400), (255, 0, 0),cv2.FILLED)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime= cTime
    cv2.putText(img,F'FPS: {int(fps)}',(40,70),cv2.FONT_HERSHEY_PLAIN,1,(255,0,255),1)
    cv2.putText(img, F'{int(volper)}%', (40, 450), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)

    cv2.imshow("Image",img)
    cv2.waitKey(1)