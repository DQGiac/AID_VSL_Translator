import cv2
from tkinter import Tk, Label, ttk, messagebox, Frame
from PIL import Image, ImageTk
import tkinter as tk
import random
import threading

labels = ["1", "2", "3", "4", "5", "6", "7", "8", "a", "b", "c", "d", "e", "g", "h", "i", "k", "l", "m", "n", "o", "p", "q", "r", "s", "space", "t", "u", "v", "x", "y"]

class VideoPlayer(threading.Thread):
    def __init__(self, video_path, img_label):
        super().__init__()
        self.video_path = video_path
        self.img_label = img_label
        self.running = True

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        while self.running:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset video to the first frame
                continue
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            img_pil = img_pil.resize((400, 400), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img_pil)
            self.img_label.config(image=img_tk)
            self.img_label.image = img_tk
            cv2.waitKey(30)  # Adjust delay as needed

        cap.release()

    def stop(self):
        self.running = False

def update_question_and_answers():
    global randc, choices
    randc = random.choice(labels)
    other_choices = random.sample([label for label in labels if label != randc], 3)
    choices = [randc] + other_choices
    random.shuffle(choices)
    
    question_label.config(text="Câu hỏi: Chọn đáp án đúng cho ký hiệu dưới đây:")
    for i, button in enumerate(answer_buttons):
        button.config(text=choices[i])

def play_video():
    global video_player
    video_path = "VSL_new/" + randc + ".mp4"
    if video_player is not None:
        video_player.stop()
    video_player = VideoPlayer(video_path, img_label)
    video_player.start()

def check_answer(answer):
    if answer == randc:
        messagebox.showinfo("Kết quả", "Bạn đã chọn đúng!")
    else:
        messagebox.showerror("Kết quả", "Bạn đã chọn sai!")

def doit():
    start_button.pack_forget()
    instructions_label.pack_forget()  # Hide instructions
    update_question_and_answers()
    for button in answer_buttons:
        button.pack(side=tk.LEFT, padx=10)
    return_button.pack(pady=20)
    play_video()
    root.update_idletasks()  # Update idle tasks to ensure window size updates
    root.geometry('')  # Adjust window size

def next():
    update_question_and_answers()
    play_video()

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

root = Tk()
root.title("Ung_dung_hoc_tap")

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TLabel", font=("Helvetica", 16))

main_frame = Frame(root)
main_frame.pack(pady=20, padx=20)

instructions_label = Label(main_frame, text="Bấm 'Start' để bắt đầu.", font=("Helvetica", 16), pady=10)
instructions_label.pack()

img_label = Label(main_frame)
img_label.pack()

question_label = Label(main_frame, text="", font=("Helvetica", 16), pady=10)
question_label.pack()

buttons_frame = Frame(main_frame)
buttons_frame.pack(pady=10)

start_button = ttk.Button(buttons_frame, text="Bắt đầu", command=doit)
start_button.pack(side=tk.LEFT, padx=10)

answer_buttons = [
    ttk.Button(buttons_frame, text="", command=lambda b=0: check_answer(answer_buttons[b].cget("text"))),
    ttk.Button(buttons_frame, text="", command=lambda b=1: check_answer(answer_buttons[b].cget("text"))),
    ttk.Button(buttons_frame, text="", command=lambda b=2: check_answer(answer_buttons[b].cget("text"))),
    ttk.Button(buttons_frame, text="", command=lambda b=3: check_answer(answer_buttons[b].cget("text")))
]

return_button = ttk.Button(buttons_frame, text="Tiếp theo", command=next)

video_player = None

center_window(root)

root.mainloop()
