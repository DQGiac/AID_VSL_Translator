import cv2
import threading
import os
from tkinter import Tk, Label, Button, StringVar, ttk, messagebox, Frame
from PIL import Image, ImageTk
import speech_recognition as sr
import time 
import subprocess
import tkinter as tk
import unicodedata
running = False

unicode_to_vni = {
    'À': 'A2', 'Á': 'A1', 'Ả': 'A3', 'Ã': 'A4', 'Ạ': 'A5',
    'Â': 'A6', 'Ầ': 'A62', 'Ấ': 'A61', 'Ẩ': 'A63', 'Ẫ': 'A64', 'Ậ': 'A65',
    'Ă': 'A8', 'Ằ': 'A82', 'Ắ': 'A81', 'Ẳ': 'A83', 'Ẵ': 'A84', 'Ặ': 'A85',
    'È': 'E2', 'É': 'E1', 'Ẻ': 'E3', 'Ẽ': 'E4', 'Ẹ': 'E5',
    'Ê': 'E6', 'Ề': 'E62', 'Ế': 'E61', 'Ể': 'E63', 'Ễ': 'E64', 'Ệ': 'E65',
    'Ì': 'I2', 'Í': 'I1', 'Ỉ': 'I3', 'Ĩ': 'I4', 'Ị': 'I5',
    'Ò': 'O2', 'Ó': 'O1', 'Ỏ': 'O3', 'Õ': 'O4', 'Ọ': 'O5',
    'Ô': 'O6', 'Ồ': 'O62', 'Ố': 'O61', 'Ổ': 'O63', 'Ỗ': 'O64', 'Ộ': 'O65',
    'Ơ': 'O7', 'Ờ': 'O72', 'Ớ': 'O71', 'Ở': 'O73', 'Ỡ': 'O74', 'Ợ': 'O75',
    'Ù': 'U2', 'Ú': 'U1', 'Ủ': 'U3', 'Ũ': 'U4', 'Ụ': 'U5',
    'Ư': 'U7', 'Ừ': 'U72', 'Ứ': 'U71', 'Ử': 'U73', 'Ữ': 'U74', 'Ự': 'U75',
    'Ỳ': 'Y2', 'Ý': 'Y1', 'Ỷ': 'Y3', 'Ỹ': 'Y4', 'Ỵ': 'Y5', "Đ": "9"
}

vocab = ["BỆNH", "BỆNHVIỆN", "CÔNG", "CÔNGAN", "BÁC", "BÁCSĨ", "ĐÚNG", "THUỐC", "XIN", "XINLỖI"]
vocab_final =["BENHVIEN", "CONGAN", "THUOC", "XINLOI", "DUNG", "BENH", "BACSI"]
def doit():
    while running:
        if os.path.exists("2_hand/text.txt"):
            with open("2_hand/text.txt", "r", encoding="utf-8") as file:
                sentence = file.read().strip().upper()
            with open("2_hand/text.txt", "w") as file:
                file.truncate(0)
        print(sentence)
        final = []
        tu = sentence.split()
        tu.append('abc')  # Call the split method with parentheses
        a = ''
        b = ''
        for char in tu:
            word_final = '' 
            a += char
            if a in vocab:
                b += char
            else:
                text_normalized = unicodedata.normalize('NFD', b)
                b = ''.join(c for c in text_normalized if unicodedata.category(c) != 'Mn')
                final.append(b)
                a = ''
                b = ''
            if a not in vocab:
                for x in char:
                    if x in unicode_to_vni:
                        word_final += unicode_to_vni[x]
                    else:
                        word_final += x
                final.append(word_final)
                a = ''
        final = [x for x in final if x != '']
        if final and final[-1] == 'abc':
            final.pop()
        print(final)
        for x in final:
            if x in vocab_final:
                print(x)
                video_path = "VSL_new/" + x.lower() + ".mp4"
                cap = cv2.VideoCapture(video_path)
                while (cap.isOpened()):
                    ret, frame = cap.read()
                    if ret==True:
                        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        img_pil = Image.fromarray(img_rgb)
                        img_pil = img_pil.resize((400, 400), Image.LANCZOS)  # Resize the image to 200x200 pixels
                        img_tk = ImageTk.PhotoImage(img_pil)
                        img_label.config(image=img_tk)
                        img_label.image = img_tk
                        # cap.grab()
                    else:
                        break
            else:
                i = 0 
                while i < len(x):
                    print(x[i])
                    video_path = "VSL_new/" + x[i].lower() + ".mp4"
                    cap = cv2.VideoCapture(video_path)
                    while (cap.isOpened()):
                        ret, frame = cap.read()
                        if ret==True:
                            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            img_pil = Image.fromarray(img_rgb)
                            img_pil = img_pil.resize((400, 400), Image.LANCZOS)  # Resize the image to 200x200 pixels
                            img_tk = ImageTk.PhotoImage(img_pil)
                            img_label.config(image=img_tk)
                            img_label.image = img_tk
                            # cap.grab()
                        else:
                            break
                    i += 1
        time.sleep(0.5)

def speech_to_text_realtime():
    microphone = sr.Microphone()
    
    while running:
        recognizer = sr.Recognizer()
        with microphone as source:
            print("Bắt đầu lắng nghe...")
            audio_stream = recognizer.listen(source)
        
        try:
            text = recognizer.recognize_google(audio_stream, language='vi-VN')
            print("Đã nghe được:", text)
            with open("2_hand/text.txt", "w", encoding="utf-8") as file:
                file.write(text)
        except sr.WaitTimeoutError:
            print("Quá thời gian chờ, không nhận được âm thanh. Đang thử lại...")
        except sr.UnknownValueError:
            print("Không nhận diện được giọng nói")
        except sr.RequestError as e:
            print(f"Lỗi trong quá trình kết nối: {e}")

def start_listening(img_label):
    window_center(root)
    global running
    if not running:
        running = True
        start_button.pack_forget()
        return_button.pack_forget()
        stop_button.pack(side=tk.LEFT, padx=10)
        return_button.pack(side=tk.LEFT, padx=10)
    threading.Thread(target=speech_to_text_realtime, daemon=True).start()
    threading.Thread(target=doit, daemon=True).start()

def stop_listening():
    global running
    running = False
    stop_button.pack_forget()
    return_button.pack_forget()
    start_button.pack(side=tk.LEFT, padx=10)
    return_button.pack(side=tk.LEFT, padx=10)
    # messagebox.showinfo("Info", "Listening stopped.")

def back():
    root.destroy()
    script_path = "2_hand/sieu_tich_hop.py"
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
    width = 700
    height = 600
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')
if __name__ == "__main__":
    root = Tk()
    root.title("Speech to Sign Language")

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)
    style.configure("TLabel", font=("Helvetica", 16))

    main_frame = Frame(root)
    main_frame.pack(pady=20, padx=20)

    instructions_label = Label(main_frame, text="Vui lòng bấm 'Bắt đầu'", font=("Helvetica", 16), pady=10)
    instructions_label.pack()

    img_label = Label(main_frame)
    img_label.pack()

    buttons_frame = Frame(main_frame)
    buttons_frame.pack(pady=10)

    start_button = ttk.Button(buttons_frame, text="Bắt đầu", command=lambda: start_listening(img_label))
    start_button.pack(side=tk.LEFT, padx=10)

    stop_button = ttk.Button(buttons_frame, text="Tạm dừng", command=stop_listening)

    return_button = ttk.Button(buttons_frame, text="Trở về", command=back)
    return_button.pack(side=tk.LEFT, padx=10)

    center_window(root)

    root.mainloop()