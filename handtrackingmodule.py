import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self,mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands( self.mode,self.maxHands,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findhands(self,img,draw=True):
        imgrgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgrgb)
        # print(self.results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    # self.mpDraw.draw_landmarks(img,handlms,self.mpHands.HAND_CONNECTIONS)
                    self.mpDraw.draw_landmarks(img, handlms)

        return img

    def findposition(self,img,handNo=0,draw=True):

        lmList=[]
        if self.results.multi_hand_landmarks:
            myHand =  self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myHand.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x *w),int(lm.y*h)
                # print(id,cx,cy)
                lmList.append([id,cx,cy])
                # if id==4:
                if draw:
                    cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
        return lmList
def main():
    c_time = 0
    p_time = 0
    vid = cv2.VideoCapture(0)
    detector=handDetector()
    while True:
        success, img = vid.read()
        img = detector.findhands(img)
        lmList = detector.findposition(img)
        if len(lmList) !=0:
            print(lmList[4])
        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ =="__main__":
    main()