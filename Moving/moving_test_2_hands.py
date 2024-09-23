import cv2
import threading
from cvzone.HandTrackingModule import HandDetector
import joblib
import time
import os
from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS
from tkinter import Tk, Label, StringVar, ttk
from tkinter import Frame
from PIL import Image, ImageTk, ImageFont, ImageDraw
import subprocess
import tkinter as tk
import pandas as pd
import numpy as np

model = joblib.load("./2_hand_model.pkl")

offset = 20
starttime = time.time()
maintext = []
disptext = ""
t = ""
running = False  
moving = ["B", "L"]

def vni_to_viet(text):
    unicode_to_vni = {
        'A2': 'À', 'A1': 'Á', 'A3': 'Ả', 'A4': 'Ã', 'A5': 'Ạ',
        'A6': 'Â', 'A62': 'Ầ', 'A61': 'Ấ', 'A63': 'Ẩ', 'A64': 'Ẫ', 'A65': 'Ậ',
        'A8': 'Ă', 'A82': 'Ằ', 'A81': 'Ắ', 'A83': 'Ẳ', 'A84': 'Ẵ', 'A85': 'Ặ',
        'E2': 'È', 'E1': 'É', 'E3': 'Ẻ', 'E4': 'Ẽ', 'E5': 'Ẹ',
        'E6': 'Ê', 'E62': 'Ề', 'E61': 'Ế', 'E63': 'Ể', 'E64': 'Ễ', 'E65': 'Ệ',
        'I2': 'Ì', 'I1': 'Í', 'I3': 'Ỉ', 'I4': 'Ĩ', 'I5': 'Ị',
        'O2': 'Ò', 'O1': 'Ó', 'O3': 'Ỏ', 'O4': 'Õ', 'O5': 'Ọ',
        'O6': 'Ô', 'O62': 'Ồ', 'O61': 'Ố', 'O63': 'Ổ', 'O64': 'Ỗ', 'O65': 'Ộ',
        'O7': 'Ơ', 'O72': 'Ờ', 'O71': 'Ớ', 'O73': 'Ở', 'O74': 'Ỡ', 'O75': 'Ợ',
        'U2': 'Ù', 'U1': 'Ú', 'U3': 'Ủ', 'U4': 'Ũ', 'U5': 'Ụ',
        'U7': 'Ư', 'U72': 'Ừ', 'U71': 'Ứ', 'U73': 'Ử', 'U74': 'Ữ', 'U75': 'Ự',
        'Y2': 'Ỳ', 'Y1': 'Ý', 'Y3': 'Ỷ', 'Y4': 'Ỹ', 'Y5': 'Ỵ', '9': 'Đ',
        "Ll": "Y TÁ ", "Bl": "XIN CHÀO "
    }
    
    vowels = "AEIOUY"  # Thêm D vào để kiểm tra 'D9' cho Đ
    numbers = "123456789"
    i = 0
    new_text = []
    
    while i < len(text):
        if text[i] in vowels and i < len(text) - 1:
            j = i + 1
            while j < len(text) and text[j] in numbers:
                j += 1
            key = "".join(text[i:j])
            if key in unicode_to_vni:
                new_text += unicode_to_vni[key]
            else:
                new_text += key
            i = j
        else:
            if text[i] in unicode_to_vni:
                text[i] = unicode_to_vni[text[i]]
            new_text += text[i]
            i += 1
    return new_text

def start_detection():
    global cap
    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=2)
    global starttime, maintext, disptext, img_label, detected_text_var, running
    xy = []
    move = ""
    start = ""
    while running:
        _, img = cap.read()
        imgOutput = img.copy()
        hands, _ = detector.findHands(img)
        if hands:
            righthand = hands[0]
            lefthand = None
            if len(hands) > 1:
                lefthand = hands[1]
                if righthand["type"] == "left":
                    lefthand, righthand = righthand, lefthand
            obj = {}
            r_x, r_y, r_w, r_h = righthand['bbox']
            r_centera, r_centerb = righthand["center"]
            nodes = [i for i in righthand["lmList"]]
            cv2.rectangle(imgOutput, (r_x - offset, r_y - offset), (r_x + r_w+offset, r_y + r_h+offset), (255, 0, 255), 4)

            for i in range(len(nodes)):
                nodes[i][0] = (nodes[i][0] - r_centera) * 1000 // r_w
                nodes[i][1] = (nodes[i][1] - r_centerb) * 1000 // r_h
                obj["r_x_" + str(i + 1)] = nodes[i][0]
                obj["r_y_" + str(i + 1)] = nodes[i][1]

            if lefthand:
                l_x, l_y, l_w, l_h = lefthand['bbox']
                l_centera, l_centerb = lefthand["center"]
                nodes = [i for i in lefthand["lmList"]]
                cv2.rectangle(imgOutput, (l_x - offset, l_y - offset), (l_x + l_w+offset, l_y + l_h+offset), (255, 0, 255), 4)
                for i in range(len(nodes)):
                    nodes[i][0] = (nodes[i][0] - l_centera) * 1000 // l_w
                    nodes[i][1] = (nodes[i][1] - l_centerb) * 1000 // l_h
                    obj["l_x_" + str(i + 1)] = nodes[i][0]
                    obj["l_y_" + str(i + 1)] = nodes[i][1]
            else:
                for i in range(1, 22):
                    obj["l_x_" + str(i)] = 0
                    obj["l_y_" + str(i)] = 0
                    
            objData = pd.DataFrame(obj, index=[0])

            a = model.predict(objData)
            label = a[0]
            if label != start:
                start = label
                xy = [nodes[0][0] + r_x, nodes[0][1] + r_y]
                # move = ""
                starttime = time.time()
            if 1 <= time.time() - starttime:
                if len(xy) == 2 and label in moving:
                    move = ""
                    if xy[0] - nodes[0][0] - r_x > r_w * 2 / 3:
                        move = "l"
                    # elif nodes[0][0] + r_x - xy[0] > r_w * 2 / 3:
                    #     move = "r"
                    # elif nodes[0][1] + r_y - xy[1] > r_h * 2 / 3:
                    #     move += "d"
                    # elif xy[1] - nodes[0][1] - r_y > r_h * 2 / 3:
                    #     move += "u"
                if label == "[cách] " and maintext != []:
                    speak(disptext)
                    maintext = []
                    disptext = ""
                    label = ""
                    move = ""
                if label + move != "":
                    if maintext != []:
                        if maintext[-1] == label + move or maintext[-1] == label:
                            maintext.pop(-1)
                    maintext.append(label + move)
                    print(label)
                    disptext = "".join(vni_to_viet(maintext))
                print('maintext', maintext)
                xy = [nodes[0][0] + r_x, nodes[0][1] + r_y]
                move = ""
                starttime = time.time()

            cv2.rectangle(imgOutput, (r_x - offset, r_y - 60),
                        (r_x + r_w + offset, r_y - 10), (255, 0, 255), -1)
            cv2_im_rgb = cv2.cvtColor(imgOutput,cv2.COLOR_BGR2RGB)
            pil_im = Image.fromarray(cv2_im_rgb)
            draw = ImageDraw.Draw(pil_im)
            font = ImageFont.truetype("Times", 40)
            draw.text((r_x + r_w // 2 - 10, r_y + r_h // 2 - 10), label, font=font, align="center")
            draw.text((20, 20), str(int((time.time() - starttime) * 100)), font=font)
            imgOutput = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
            cv2.rectangle(imgOutput, (r_x - offset, r_y - offset), (r_x + r_w + offset, r_y + r_h + offset), (255, 0, 255), 4)
        img_rgb = cv2.cvtColor(imgOutput, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(image=img_pil)
        img_label.config(image=img_tk)
        img_label.image = img_tk

        detected_text_var.set(disptext)

def speak(text):
    tts = gTTS(text=text, lang="vi", slow=False)
    tts.save("sound.mp3")
    song = AudioSegment.from_mp3("sound.mp3")
    play(song)
    os.remove("sound.mp3")


"""

    UI things

"""


def start_detection_thread():
    global running
    running = True
    start_button.pack_forget()
    return_button.pack_forget()
    stop_button.pack(side=tk.LEFT, padx=10)
    return_button.pack(side=tk.LEFT, padx=10)
    threading.Thread(target=start_detection).start()

def auto_start_detection():
    center_window(root)
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
    if cap: cap.release()
    cv2.destroyAllWindows()
    script_path = "sieu_tich_hop.py"
    subprocess.run(["python", script_path])

def center_window(window):
    window.update_idletasks()
    # width = window.winfo_width()
    # height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = 0
    y = 0
    window.geometry(f'{screen_width}x{screen_height}+{x}+{y}')

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