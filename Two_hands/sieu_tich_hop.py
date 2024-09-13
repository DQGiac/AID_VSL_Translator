import tkinter as tk
from tkinter import ttk
import subprocess
from tkinter import *

def open_interface_1():
    root.destroy()
    script_path = "speech_to_hand.py"
    subprocess.run(["python", script_path])

def open_interface_2():
    root.destroy()
    script_path = "hand_to_speech.py"
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

root = tk.Tk()
root.title("Main Interface")

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 14), padding=10)
style.configure("TLabel", font=("Helvetica", 18, "bold"))

main_frame = tk.Frame(root)
main_frame.pack(pady=20, padx=20)

title_label = ttk.Label(main_frame, text="Chương trình")
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

buttons_frame = tk.Frame(main_frame)
buttons_frame.grid(row=1, column=0, columnspan=2)

button1 = ttk.Button(buttons_frame, text="Speech to Hand", command=open_interface_1)
button1.grid(row=0, column=0, padx=20)

button2 = ttk.Button(buttons_frame, text="Hand to Speech", command=open_interface_2)
button2.grid(row=0, column=1, padx=20)

center_window(root)

root.mainloop()
