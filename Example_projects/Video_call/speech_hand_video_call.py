import tkinter as tk
import threading
import subprocess
from tkinter import Tk, ttk, Frame

def run_script(script_name):
    return subprocess.Popen(["python", script_name])

def start_scripts():
    global script1_process, script2_process, running
    if not running:
        running = True
        script1_process = run_script("video call/imgage_adding.py")
        script2_process = run_script("video call/vir_cam_speech.py")

        start_button.config(text="Tạm dừng", command=stop_scripts)

def stop_scripts():
    global running
    if running:
        running = False
        if script1_process:
            script1_process.terminate()
        if script2_process:
            script2_process.terminate()

        start_button.config(text="Bắt đầu", command=start_scripts)

def back():
    root.destroy()
    if script1_process:
        script1_process.terminate()
    if script2_process:
        script2_process.terminate()
    script_path = "video call/siêu_tích_hợp_video_call.py"
    subprocess.run(["python", script_path])

# Khởi tạo giao diện tkinter
root = Tk()
root.title("Phiên dịch ngôn ngữ nói")

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TLabel", font=("Helvetica", 16))

main_frame = Frame(root)
main_frame.pack(pady=20, padx=20)

instruction_label = ttk.Label(main_frame, text="Vui lòng bấm 'Bắt đầu'")
instruction_label.pack(pady=(0, 10))

buttons_frame = Frame(main_frame)
buttons_frame.pack(pady=10)

start_button = ttk.Button(buttons_frame, text="Bắt đầu", command=start_scripts)
start_button.pack(side=tk.LEFT, padx=10)

return_button = ttk.Button(buttons_frame, text="Trở về", command=back)
return_button.pack(side=tk.LEFT, padx=10)

running = False
script1_process = None
script2_process = None

root.mainloop()