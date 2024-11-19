import tkinter as tk
from tkinter import ttk
import subprocess

# Định nghĩa giao diện 1 (code đầu tiên của bạn)
def open_interface_1():
    root.destroy()
    script_path = "2_hand/speech_to_hand_app.py"
    subprocess.run(["python", script_path])

# Định nghĩa giao diện 2 (code thứ hai của bạn)
def open_interface_2():
    root.destroy()
    script_path = "2_hand/hand_speech_final.py"
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

# Giao diện chính để dẫn đến hai đoạn mã của bạn
root = tk.Tk()
root.title("Giao diện chính")

# Load icons for buttons
icon1 = tk.PhotoImage(file="2_hand/assets/icon1.png")  # Replace with your actual path to icon1
icon2 = tk.PhotoImage(file="2_hand/assets/icon2.png")  # Replace with your actual path to icon2

# Style configuration
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 14), padding=10)
style.configure("TLabel", font=("Helvetica", 18, "bold"))

# Main frame
main_frame = tk.Frame(root)
main_frame.pack(pady=20, padx=20)

# Label for title
title_label = ttk.Label(main_frame, text="Chương trình")
title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))

# Buttons frame
buttons_frame = tk.Frame(main_frame)
buttons_frame.grid(row=1, column=0, columnspan=4)

# Button for interface 1 with icon
button1 = ttk.Button(buttons_frame, text="Phiên dịch giọng nói", command=open_interface_1)
button1.config(image=icon1, compound="left")  # Add the icon to button1
button1.grid(row=0, column=0, padx=20)

# Button for interface 2 with icon
button2 = ttk.Button(buttons_frame, text="Phiên dịch ngôn ngữ kí hiệu", command=open_interface_2)
button2.config(image=icon2, compound="left")  # Add the icon to button2
button2.grid(row=0, column=1, padx=20)

center_window(root)

# Keep references to icons
root.icon1 = icon1
root.icon2 = icon2

root.mainloop()
