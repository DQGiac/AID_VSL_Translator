import cv2
import threading
from cvzone.HandTrackingModule import HandDetector
import joblib
import time
import os
from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS
from tkinter import Tk, Label, Button, StringVar, ttk, Frame
from PIL import Image, ImageTk
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import subprocess
import tkinter as tk
import pandas as pd

language = 'vi'

model = joblib.load("lgbm_model.pkl")

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
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
    if os.path.getsize("sound.mp3") != 0:
        print(os.path.getsize("sound.mp3"))
        # AudioSegment.converter = "/path/to/ffmpeg"
        song = AudioSegment.from_mp3("sound.mp3")
        play(song)

def start_detection():
    global start, starttime, maintext, img_label, detected_text_var, running
    while running:
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
            label = a[0]
            if label != start:
                start = label
                starttime = time.time()
            if (time.time() - starttime >= 1):
                if label == "space":
                    if maintext != "":
                        maintext = vni_to_viet(maintext)
                        print(maintext)
                        speak(maintext)
                        maintext = ""
                        starttime = time.time()
                else:
                    maintext += label
                    starttime = time.time()
            print(maintext, time.time() - starttime)

            # cv2.rectangle(imgOutput, (x - offset, y - 60),
            #             (x + w + offset, y - 10), (255, 0, 255), -1)
            cv2.putText(imgOutput, a[0], (x + w // 2 - 10, y + h // 2 - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(imgOutput, maintext, (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.2 if len(t) < 10 else 1.2 - len(t) * 0.03, (255, 255, 255), 2)
            cv2.rectangle(imgOutput, (x-offset, y-offset),
                        (x + w+offset, y + h+offset), (255, 0, 255), 4)

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
