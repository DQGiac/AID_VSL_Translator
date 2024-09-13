import cv2
import subprocess
from cvzone.HandTrackingModule import HandDetector
# from cvzone.ClassificationModule import Classifier
import numpy as np
import pandas as pd
import math
import time 
import os
import joblib
from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS
# from webdriver_manager.chrome import ChromeDriverManager

model = joblib.load("lgbm_model.pkl")

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
offset = 20
imgSize = 300
counter = 0
labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "G", "H", "I", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "space", "T", "U", "V", "X", "Y"]
start = ""
starttime = time.time()
maintext = ""
n = 0
t = ""

language="vi"

def speak(text):
    # print("Bot: {}".format(text))
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("sound.mp3")
    song = AudioSegment.from_mp3("sound.mp3")
    play(song)
    os.remove("sound.mp3")

while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    arr = []
    cols = ["x_1", "y_1", "x_2", "y_2", "x_3", "y_3", "x_4", "y_4", "x_5", "y_5", "x_6", "y_6", "x_7", "y_7", "x_8", "y_8", "x_9", "y_9", "x_10", "y_10", "x_11", "y_11", "x_12", "y_12", "x_13", "y_13", "x_14", "y_14", "x_15", "y_15", "x_16", "y_16", "x_17", "y_17", "x_18", "y_18", "x_19", "y_19", "x_20", "y_20", "x_21", "y_21"]
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        centera, centerb = hands[0]["center"]
        nodes = [i for i in hands[0]["lmList"]]
        obj = {}
        for i in range(len(nodes)):
            nodes[i][0] = (nodes[i][0] - centera) * 1000 // w
            nodes[i][1] = (nodes[i][1] - centerb) * 1000 // h
            obj["x_" + str(i + 1)] = nodes[i][0]
            obj["y_" + str(i + 1)] = nodes[i][1]
        objData = pd.DataFrame(obj, index=[0])
        a = model.predict(objData)
        # print(a)
        # print(a[0])
        # print(t)
        print(time.time() - starttime)
        if a[0] != start:
            starttime = time.time()
            start = a[0]
        if time.time() - starttime > 1:
            if a[0] == "space": t = ""
            else: t += a[0]
            starttime = time.time()
        # imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        # imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
        # imgCropShape = imgCrop.shape
        # aspectRatio = h / w
        # if aspectRatio > 1:
        #     k = imgSize / h
        #     wCal = math.ceil(k * w)
        #     imgResize = cv2.resize(imgCrop, (wCal, imgSize))
        #     imgResizeShape = imgResize.shape
        #     wGap = math.ceil((imgSize - wCal) / 2)
        #     imgWhite[:, wGap:wCal + wGap] = imgResize
        # else:
        #     k = imgSize / w
        #     hCal = math.ceil(k * h)
        #     imgResize = cv2.resize(imgCrop, (imgSize, hCal))
        #     imgResizeShape = imgResize.shape
        #     hGap = math.ceil((imgSize - hCal) / 2)
        #     imgWhite[hGap:hCal + hGap, :] = imgResize
        cv2.rectangle(imgOutput, (x - offset, y - 60),
                    (x + w + offset, y - 10), (255, 0, 255), -1)
        cv2.putText(imgOutput, a[0], (x + w // 2 - 10, y + h // 2 - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(imgOutput, t, (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.2 if len(t) < 10 else 1.2 - len(t) * 0.03, (255, 255, 255), 2)
        cv2.rectangle(imgOutput, (x-offset, y-offset),
                    (x + w+offset, y + h+offset), (255, 0, 255), 4)
        
        # cv2.rectangle(imgOutput, (x-offset, y-offset),
        #           (x + w+offset, y + h+offset), (255, 0, 255), 4)

        # for i in range(len(hands[0]["lmList"])):
        #     _center = (hands[0]["lmList"][i][0], hands[0]["lmList"][i][1])
        #     # print(_center)
        #     cv2.circle(imgOutput, _center, 10, (255, i * 20, 0), -1)
        # cv2.imshow("ImageCrop", imgCrop)
        # cv2.imshow("ImageWhite", imgWhite)
    # else: space
    
    cv2.imshow("Image", imgOutput)
    key = cv2.waitKey(1)
    if key == ord("1"):
        # if csv_1_hand == []:
        # df.to_csv("csv_1_hand.csv", index=False)
        # else:
        #     pd.concat([df, pd.read_csv("csv_1_hand.csv")]).to_csv("csv_1_hand.csv")
        cv2.destroyAllWindows()
        break