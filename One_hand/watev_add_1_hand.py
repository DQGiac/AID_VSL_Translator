import cv2
import subprocess
from cvzone.HandTrackingModule import HandDetector
# from cvzone.ClassificationModule import Classifier
import numpy as np
import pandas as pd
import math
import os

language = 'vi'
# csv_1_hand = pd.read_csv("csv_1_hand.csv")

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
# classifier = Classifier("keras_model.h5", "labels.txt")
offset = 20
imgSize = 300
# folder = "E:\\Software\\AI python\\HandSignDetection\\Data"
counter = 0
labels = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "A", "B", "C", "D", "E", "G", "H", "I", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "space", "T", "U", "V", "X", "Y"]
start = -1
maintext = ""
df = ""
# csv_1_hand = []
n = 0
if os.path.getsize("csv_1_hand.csv") != 0:
    df = pd.read_csv("csv_1_hand.csv")
    n = len(df)


target = "9"


while True:
    success, img = cap.read()
    # img = img.ksjdfksld
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
        obj["target"] = target
        # if type(df) == str:
        #     df = pd.DataFrame(obj, index=[0])
        # else:
        #     df = pd.concat([df, pd.DataFrame(obj, index=[len(df)])])
        # nodes[i][0] = nodes[]
        # print(nodes[:7])
        # arr += obj
        # print(df)
        # df = pd.DataFrame(arr, index=[i for i in range(len(arr))])
        # csv_1_hand = pd.read_csv("csv_1_hand.csv")
        # df = csv_1_hand + df
        # print(df)

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
        imgCropShape = imgCrop.shape
        aspectRatio = h / w
        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize
        # cv2.rectangle(imgOutput, (x - offset, y - offset-50),
        #             (x - offset+90, y - offset-50+50), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgOutput, maintext, (x, y -26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
        cv2.rectangle(imgOutput, (x-offset, y-offset),
                    (x + w+offset, y + h+offset), (255, 0, 255), 4)
        cv2.rectangle(imgOutput, (x-offset, y-offset),
                    (x + w+offset, y + h+offset), (255, 0, 255), 4)
        if cv2.waitKey(1) == ord("s"):
            if type(df) == str:
                df = pd.DataFrame(obj, index=[0])
            else:
                df = pd.concat([df, pd.DataFrame(obj, index=[len(df)])])
            n += 1
            print(n, target)

        # for i in range(len(hands[0]["lmList"])):
        #     _center = (hands[0]["lmList"][i][0], hands[0]["lmList"][i][1])
        #     # print(_center)
        #     cv2.circle(imgOutput, _center, 10, (255, i * 20, 0), -1)
        # cv2.imshow("ImageCrop", imgCrop)
        cv2.imshow("ImageWhite", imgWhite)
    cv2.imshow("Image", imgOutput)
    key = cv2.waitKey(1)
    if key == ord("1"):
        # if csv_1_hand == []:
        df.to_csv("csv_1_hand.csv", index=False)
        # else:
        #     pd.concat([df, pd.read_csv("csv_1_hand.csv")]).to_csv("csv_1_hand.csv")
        cv2.destroyAllWindows()
        break