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
# from webdriver_manager.chrome import ChromeDriverManager

model = joblib.load("2_hand_model.pkl")

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=2)
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

while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    cols = ["r_x_1", "r_y_1", "r_x_2", "r_y_2", "r_x_3", "r_y_3", "r_x_4", "r_y_4", "r_x_5", "r_y_5",
            "r_x_6", "r_y_6", "r_x_7", "r_y_7", "r_x_8", "r_y_8", "r_x_9", "r_y_9", "r_x_10", "r_y_10",
            "r_x_11", "r_y_11", "r_x_12", "r_y_12", "r_x_13", "r_y_13", "r_x_14", "r_y_14", "r_x_15", "r_y_15",
            "r_x_16", "r_y_16", "r_x_17", "r_y_17", "r_x_18", "r_y_18", "r_x_19", "r_y_19", "r_x_20", "r_y_20",
            "r_x_21", "r_y_21","l_x_1", "l_y_1", "l_x_2", "l_y_2", "l_x_3", "l_y_3", "l_x_4", "l_y_4", "l_x_5",
            "l_y_5", "l_x_6", "l_y_6", "l_x_7", "l_y_7", "l_x_8", "l_y_8", "l_x_9", "l_y_9", "l_x_10", "l_y_10",
            "l_x_11", "l_y_11", "l_x_12", "l_y_12", "l_x_13", "l_y_13", "l_x_14", "l_y_14", "l_x_15", "l_y_15",
            "l_x_16", "l_y_16", "l_x_17", "l_y_17", "l_x_18", "l_y_18", "l_x_19", "l_y_19", "l_x_20", "l_y_20",
            "l_x_21", "l_y_21", "target"]
    if hands:
        righthand = hands[0]
        lefthand = None
        if len(hands) > 1:
            lefthand = hands[1]
            if righthand["type"] == "left":
                lefthand, righthand = righthand, lefthand
        r_x, r_y, r_w, r_h = righthand['bbox']
        r_centera, r_centerb = righthand["center"]
        nodes = [i for i in righthand["lmList"]]
        obj = {}
        cv2.rectangle(imgOutput, (r_x-offset, r_y-offset), (r_x + r_w+offset, r_y + r_h+offset), (255, 0, 255), 4)
        cv2.putText(imgOutput, righthand["type"], [r_x, r_y], cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255))

        for i in range(len(nodes)):
            nodes[i][0] = (nodes[i][0] - r_centera) * 1000 // r_w
            nodes[i][1] = (nodes[i][1] - r_centerb) * 1000 // r_h
            obj["r_x_" + str(i + 1)] = nodes[i][0]
            obj["r_y_" + str(i + 1)] = nodes[i][1]

        if lefthand:
            l_x, l_y, l_w, l_h = lefthand['bbox']
            l_centera, l_centerb = lefthand["center"]
            nodes = [i for i in lefthand["lmList"]]
            cv2.rectangle(imgOutput, (l_x-offset, l_y-offset), (l_x + l_w+offset, l_y + l_h+offset), (255, 0, 255), 4)
            cv2.putText(imgOutput, lefthand["type"], [l_x, l_y], cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255))
            for i in range(len(nodes)):
                nodes[i][0] = (nodes[i][0] - l_centera) * 1000 // l_w
                nodes[i][1] = (nodes[i][1] - l_centerb) * 1000 // l_h
                obj["l_x_" + str(i + 1)] = nodes[i][0]
                obj["l_y_" + str(i + 1)] = nodes[i][1]
        print(obj)

        if "l_x_1" not in obj:
            for i in range(1, 22):
                obj["l_x_" + str(i)] = 0
                obj["l_y_" + str(i)] = 0
                
        objData = pd.DataFrame(obj, index=[0])
        a = model.predict(objData)
        print(time.time() - starttime)
        if a[0] != start:
            starttime = time.time()
            start = a[0]
        if time.time() - starttime > 1:
            if a[0] == "space": t = ""
            else: t += a[0]
            starttime = time.time()
        # cv2.rectangle(imgOutput, (r_x - offset, r_y - 60),
        #             (r_x + r_w + offset, r_y - 10), (255, 0, 255), -1)
        cv2.putText(imgOutput, a[0], (r_x + r_w // 2 - 10, r_y + r_h // 2 - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(imgOutput, t, (r_x, r_y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.2 if len(t) < 10 else 1.2 - len(t) * 0.03, (255, 255, 255), 2)
        
    cv2.imshow("Image", imgOutput)
    key = cv2.waitKey(1)
    if key == ord("1"):
        cv2.destroyAllWindows()
        break