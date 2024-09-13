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

language = 'vi'

model = joblib.load("2_hand_model.pkl")

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

# listImg = os.listdir("BackgroundImages")
# imgList = []
# for imgPath in listImg:
#     img = cv2.imread(f'BackgroundImages/{imgPath}')
#     imgList.append(img)

segmentor = SelfiSegmentation()
indexImg = 0

def vni_to_viet(text):
    unicode_to_vni = {
        'A2': 'À', 'A1': 'Á', 'A3': 'Ả', 'A4': 'Ã', 'A5': 'Ạ',
        'A6': 'Â', 'A62': 'Ầ', 'A61': 'Ấ', 'A63': 'Ẩ', 'A64': 'Ẫ', 'A65': 'Ậ',
        'A8': 'Ă', 'A82': 'Ằ', 'A81': 'Ắ', 'A83': 'Ẳ', 'A84': 'Ẵ', 'A85': 'Ặ',
        'E2': 'Ặ', 'E1': 'É', 'E3': 'Ẻ', 'E4': 'Ẽ', 'E5': 'Ẹ',
        'E6': 'Ê', 'E62': 'Ề', 'E61': 'Ế', 'E63': 'Ể', 'E64': 'Ễ', 'E65': 'Ệ',
        'I2': 'Ì', 'I1': 'Í', 'I3': 'Ỉ', 'I4': 'Ĩ', 'I5': 'Ị',
        'O2': 'Ò', 'O1': 'Ó', 'O3': 'Ỏ', 'O4': 'Õ', 'O5': 'Ọ',
        'O6': 'Ô', 'O62': 'Ồ', 'O61': 'Ố', 'O63': 'Ổ', 'O64': 'Ỗ', 'O65': 'Ộ',
        'O7': 'Ơ', 'O72': 'Ờ', 'O71': 'Ớ', 'O73': 'Ở', 'O74': 'Ỡ', 'O75': 'Ợ',
        'U2': 'Ù', 'U1': 'Ú', 'U3': 'Ủ', 'U4': 'Ũ', 'U5': 'Ụ',
        'U7': 'Ư', 'U72': 'Ừ', 'U71': 'Ứ', 'U73': 'Ử', 'U74': 'Ữ', 'U75': 'Ự',
        'Y2': 'Ỳ', 'Y1': 'Ý', 'Y3': 'Ỷ', 'Y4': 'Ỹ', 'Y5': 'Ỵ'
    }
    vowels = "AEIOUY"
    numbers = "12345678"
    i = 0
    new_text = ""
    while i < len(text):
        if text[i] == "9":
            new_text += "Đ"
            continue
        elif text[i] in vowels:
            j = i + 1
            while j < len(text):
                if text[j] not in numbers:
                    break
                j += 1
            new_text += unicode_to_vni[text[i:j]] if j > i + 1 else text[i]
            i = j - 1
        else:
            new_text += text[i]
        i += 1
    return new_text

def speak(text):
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("sound.mp3")
    song = AudioSegment.from_mp3("sound.mp3")
    play(song)
    os.remove("sound.mp3")

def start_detection():
    global start, starttime, maintext, img_label, detected_text_var, running
    while running:
        _, img = cap.read()
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
            if len(hands) == 2:
                lefthand = hands[1]
                if righthand["type"] == "left":
                    lefthand, righthand = righthand, lefthand
            r_x, r_y, r_w, r_h = righthand['bbox']
            r_centera, r_centerb = righthand["center"]
            nodes = [i for i in righthand["lmList"]]
            obj = {}
            cv2.rectangle(imgOutput, (r_x-offset, r_y-offset), (r_x + r_w+offset, r_y + r_h+offset), (255, 0, 255), 4)
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
                cv2.rectangle(imgOutput, (l_x-offset, l_y-offset), (l_x + l_w+offset, l_y + l_h+offset), (255, 0, 255), 4)
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
            label = a[0]
            if label != start:
                start = label
                starttime = time.time()
            if (time.time() - starttime >= 0.7):
                if label != "space":
                    maintext += label
                    starttime = time.time()
                    print(maintext, time.time() - starttime)
                elif maintext != "":
                    maintext = vni_to_viet(maintext)
                    speak(maintext)
                    maintext = ""
            cv2.putText(imgOutput, a[0], (r_x + r_w // 2 - 10, r_y + r_h // 2 - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        else:
            starttime = time.time()
        img_rgb = cv2.cvtColor(imgOutput, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(image=img_pil)
        img_label.config(image=img_tk)
        img_label.image = img_tk

        detected_text_var.set(maintext)

def start_detection_thread():
    global running
    running = True
    start_button.pack_forget()
    return_button.pack_forget()
    stop_button.pack(side=tk.LEFT, padx=10)
    return_button.pack(side=tk.LEFT, padx=10)
    threading.Thread(target=start_detection).start()

def auto_start_detection():
    window_center(root)
    root.after(50, start_detection_thread)  

def stop_detection():
    global running
    running = False
    stop_button.pack_forget()
    return_button.pack_forget()
    start_button.pack(side=tk.LEFT, padx=10)
    return_button.pack(side=tk.LEFT, padx=10)

def back():
    root.destroy()
    cap.release()
    cv2.destroyAllWindows()
    script_path = "sieu_tich_hop.py"
    subprocess.run(["python", script_path])

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
root.title("Hand Sign Detection")

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TLabel", font=("Helvetica", 16))

main_frame = Frame(root)
main_frame.pack(pady=20, padx=20)

img_label = Label(main_frame)
img_label.pack()

detected_text_var = StringVar()
detected_text_var.set("Detected text will appear here")

detected_text_label = Label(main_frame, textvariable=detected_text_var, font=("Helvetica", 16), pady=10)
detected_text_label.pack()

buttons_frame = Frame(main_frame)
buttons_frame.pack(pady=10)

start_button = ttk.Button(buttons_frame, text="Start Detection", command=auto_start_detection)
start_button.pack(side=tk.LEFT, padx=10)

stop_button = ttk.Button(buttons_frame, text="Stop Detection", command=stop_detection)

return_button = ttk.Button(buttons_frame, text="Return", command=back)
return_button.pack(side=tk.LEFT, padx=10)

center_window(root)

root.mainloop()