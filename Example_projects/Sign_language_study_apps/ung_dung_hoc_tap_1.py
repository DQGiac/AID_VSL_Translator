import cv2
import threading
from cvzone.HandTrackingModule import HandDetector
import joblib
import time
import os
from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS
from tkinter import Tk, Label, Button, StringVar, ttk
from tkinter import Frame
from PIL import Image, ImageTk
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import subprocess
import tkinter as tk
import pandas as pd
import random
import unicodedata

language = 'vi'

model = joblib.load("2_hand/2_hand_model.pkl")

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=2)
offset = 20
imgSize = 300
counter = 0
start = ""
starttime = time.time()
maintext = ""
n = 0
t = ""
running = False  

labels = ["2", "3", "4", "5", "6", "7", "8", "B", "C", "D", "E", "G", "H", "I", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "space", "T", "U", "V", "X", "Y", "BỆNH", "BÁC SĨ", "BỆNH VIỆN", "ĐAU", "THUỐC", "ĐÚNG", "CÓ"]
label_check = ["BỆNH", "BÁC SĨ", "BỆNH VIỆN", "ĐAU", "THUỐC", "ĐÚNG", "CÓ"]
rand = random.randint(0, len(labels)-1)

def start_detection():
    global start, starttime, maintext, img_label, detected_text_var, running
    q = 255
    p = 0
    r = 255 
    while running:
        _, img = cap.read()
        imgOutput = img.copy()
        hands, img = detector.findHands(img)
        if hands:
            righthand = hands[0]
            lefthand = None
            if len(hands) == 2:
                lefthand = hands[1]
                if righthand["type"] == "left":
                    lefthand, righthand = righthand, lefthand
            r_x, r_y, r_w, r_h = righthand['bbox']
            r_centera, r_centerb = righthand["center"]
            nodes = [i for i in righthand["lmList"]]
            obj = {}
            cv2.rectangle(imgOutput, (r_x-offset, r_y-offset), (r_x + r_w+offset, r_y + r_h+offset), (q, p, r), 4)
            # cv2.putText(imgOutput, righthand["type"], [r_x, r_y], cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255))

            for i in range(len(nodes)):
                nodes[i][0] = (nodes[i][0] - r_centera) * 1000 // r_w
                nodes[i][1] = (nodes[i][1] - r_centerb) * 1000 // r_h
                obj["r_x_" + str(i + 1)] = nodes[i][0]
                obj["r_y_" + str(i + 1)] = nodes[i][1]

            if lefthand:
                l_x, l_y, l_w, l_h = lefthand['bbox']
                l_centera, l_centerb = lefthand["center"]
                nodes = [i for i in lefthand["lmList"]]
                cv2.rectangle(imgOutput, (l_x-offset, l_y-offset), (l_x + l_w+offset, l_y + l_h+offset), (q, p, r), 4)
                # cv2.putText(imgOutput, lefthand["type"], [l_x, l_y], cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255))

                for i in range(len(nodes)):
                    nodes[i][0] = (nodes[i][0] - l_centera) * 1000 // l_w
                    nodes[i][1] = (nodes[i][1] - l_centerb) * 1000 // l_h
                    obj["l_x_" + str(i + 1)] = nodes[i][0]
                    obj["l_y_" + str(i + 1)] = nodes[i][1]
            else:
                for i in range(1, 22):
                    obj["l_x_" + str(i)] = 0
                    obj["l_y_" + str(i)] = 0
            # print(obj)
            objData = pd.DataFrame(obj, index=[0])
            a = model.predict(objData)
            if a != labels[rand]:
                q = 0
                p = 0
                r = 255
            else:
                q = 0
                p = 255
                r = 0

        img_rgb = cv2.cvtColor(imgOutput, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(image=img_pil)
        img_label.config(image=img_tk)
        img_label.image = img_tk

        root.update_idletasks()
        root.update()

def start_detection_thread():
    global running, rand
    running = True
    rand = random.randint(1, 10)
    text = "Hãy giơ chữ {}".format(labels[rand])
    detected_text_var.set(text)
    start_button.pack_forget()
    return_button.pack_forget()
    next_button.pack(side=tk.LEFT, padx=10)
    return_button.pack(side=tk.LEFT, padx=10)
    threading.Thread(target=start_detection).start()

def auto_start_detection():
    window_center(root)
    root.after(50, start_detection_thread)  

def next():
    global rand
    rand = random.randint(0, len(labels) - 1)
    text = "Hãy giơ chữ {}".format(labels[rand])
    detected_text_var.set(text)

def Answer():
    original_file_path = 'video.MP4'
    if labels[rand] in label_check:
        nfkd_form = unicodedata.normalize('NFKD', labels[rand])
        result = ''.join([c for c in nfkd_form if not unicodedata.combining(c)]).replace(" ", "")
        print(result)
        new_file_path = f'VSL_new/{result}.MP4'
    else:
        new_file_path = f'VSL_new/{labels[rand]}.MP4'

    with open(new_file_path, 'rb') as nf:
        new_content = nf.read()

    # Ghi đè nội dung mới lên file gốc
    with open(original_file_path, 'wb') as of:
        of.write(new_content)

    script_path = "hoc_tap/answer.py"
    subprocess.Popen(["python", script_path])

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def window_center(window):
    window.update_idletasks()
    width = 800
    height = 650
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

root = Tk()
root.title("Ứng dụng học tập")

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TLabel", font=("Helvetica", 16))

main_frame = Frame(root)
main_frame.pack(pady=20, padx=20)

detected_text_var = StringVar()
detected_text_var.set("Vui lòng bấm 'Bắt đầu' ")

detected_text_label = Label(main_frame, textvariable=detected_text_var, font=("Helvetica", 16), pady=10)
detected_text_label.pack()

img_label = Label(main_frame)
img_label.pack()

buttons_frame = Frame(main_frame)
buttons_frame.pack(pady=10)

start_button = ttk.Button(buttons_frame, text="Bắt đầu", command=auto_start_detection)
start_button.pack(side=tk.LEFT, padx=10)

next_button = ttk.Button(buttons_frame, text="Tiếp theo", command=next)

return_button = ttk.Button(buttons_frame, text="Đáp án", command=Answer)

center_window(root)

root.mainloop()
