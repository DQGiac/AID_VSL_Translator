import cv2
from PIL import Image
running = False

sign = " 53412"
alphabet = "abcdeghiklmnopqrstuvxy" + sign
accented = ["aạảãáà", "eẹẻẽéè", "iịỉĩíì", "oọỏõóò", "uụủũúù", "ăặẳẵắằ", "âậẩẫấầ", "êệểễếề", "ôộổỗốồ", "ơợởỡớờ", "ưựửữứừ"]

def doit(word):
    i = 0
    uniword = word
    while i < len(uniword):
        if uniword[i] not in alphabet:
            for ind in range(5):
                if uniword[i] in accented[ind]:
                    ind1 = accented[ind].index(uniword[i])
                    uniword = uniword[:i] + accented[ind][0] + sign[ind1] + uniword[i + 1:]
            if uniword[i] in accented[5]:
                ind = accented[5].index(uniword[i])
                if ind == 0:
                    uniword = uniword[:i] + "a8" + uniword[i + 1:]
                else:
                    uniword = uniword[:i] + "a8" + sign[ind] + uniword[i + 1:]
            elif uniword[i] in accented[6]:
                ind = accented[6].index(uniword[i])
                if ind == 0:
                    uniword = uniword[:i] + "a6" + uniword[i + 1:]
                else:
                    uniword = uniword[:i] + "a6" + sign[ind] + uniword[i + 1:]
            elif uniword[i] in accented[7]:
                ind = accented[7].index(uniword[i])
                if ind == 0:
                    uniword = uniword[:i] + "e6" + uniword[i + 1:]
                else:
                    uniword = uniword[:i] + "e6" + sign[ind] + uniword[i + 1:]
            elif uniword[i] in accented[8]:
                ind = accented[8].index(uniword[i])
                if ind == 0:
                    uniword = uniword[:i] + "o6" + uniword[i + 1:]
                else:
                    uniword = uniword[:i] + "o6" + sign[ind] + uniword[i + 1:]
            elif uniword[i] in accented[9]:
                ind = accented[9].index(uniword[i])
                if ind == 0:
                    uniword = uniword[:i] + "o7" + uniword[i + 1:]
                else:
                    uniword = uniword[:i] + "o7" + sign[ind] + uniword[i + 1:]
            elif uniword[i] in accented[10]:
                ind = accented[10].index(uniword[i])
                if ind == 0:
                    uniword = uniword[:i] + "u7" + uniword[i + 1:]
                else:
                    uniword = uniword[:i] + "u7" + sign[ind] + uniword[i + 1:]
            if uniword[i] == "đ":
                uniword = uniword[:i] + "8" + uniword[i + 1:]
        img = cv2.VideoCapture('video/' + uniword[i].upper() + ".mov")
        # img = img.crop(0, img.width, 200, 200 + img.width)
        cv2.imshow(word, img)
        cv2.waitKey(400)

    if cv2.waitKey(1) == 27:
        exit(0)

        # if os.path.exists(img_path):
        #     img = cv2.imread(img_path)
        #     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #     img_pil = Image.fromarray(img_rgb)
        #     img_pil = img_pil[200:, 0:]
        #     img_tk = ImageTk.PhotoImage(img_pil)
        # else:
        #     print(f"Image not found for character: {uniword[i]}")
        # time.sleep(0.4) 
        i += 1
    return False

a = input()
print(doit(a))
# def speech_to_text_realtime():
#     recognizer = sr.Recognizer()
#     microphone = sr.Microphone()

#     with microphone as source:
#         print("Bắt đầu lắng nghe...")
#         audio_stream = recognizer.listen(source)

#     try:
#         text = recognizer.recognize_google(audio_stream, language='vi-VN').split(" ")
#         print("Đã nghe được:", recognizer.recognize_google(audio_stream, language='vi-VN'))
#         return text
#     except sr.UnknownValueError:
#         print("Không nhận diện được giọng nói")
#         return False
#     except sr.RequestError as e:
#         print(f"Lỗi trong quá trình kết nối: {e}")
#         return False

# def main_loop(img_label):
#     while running:
#         text = speech_to_text_realtime()
#         if text:
#             for word in text:
#                 if not running: 
#                     break
#                 if doit(word, img_label):
#                     break

# def start_listening(img_label):
#     window_center(root)
#     global running
#     if not running:
#         running = True
#         start_button.pack_forget()
#         return_button.pack_forget()
#         stop_button.pack(side=tk.LEFT, padx=10)
#         return_button.pack(side=tk.LEFT, padx=10)
#         threading.Thread(target=main_loop, args=(img_label,)).start()

# def stop_listening():
#     global running
#     running = False
#     stop_button.pack_forget()
#     return_button.pack_forget()
#     start_button.pack(side=tk.LEFT, padx=10)
#     return_button.pack(side=tk.LEFT, padx=10)
#     # messagebox.showinfo("Info", "Listening stopped.")

# def back():
#     root.destroy()
#     script_path = "sieu_tich_hop.py"
#     subprocess.run(["python", script_path])

# def center_window(window):
#     window.update_idletasks()
#     width = window.winfo_width()
#     height = window.winfo_height()
#     screen_width = window.winfo_screenwidth()
#     screen_height = window.winfo_screenheight()
#     x = (screen_width // 2) - (width // 2)
#     y = (screen_height // 2) - (height // 2)
#     window.geometry(f'{width}x{height}+{x}+{y}')

# def window_center(window):
#     window.update_idletasks()
#     width = 700
#     height = 600
#     screen_width = window.winfo_screenwidth()
#     screen_height = window.winfo_screenheight()
#     x = (screen_width // 2) - (width // 2)
#     y = (screen_height // 2) - (height // 2)
#     window.geometry(f'{width}x{height}+{x}+{y}')

# root = Tk()
# root.title("Speech to Sign Language")

# style = ttk.Style()
# style.configure("TButton", font=("Helvetica", 12), padding=10)
# style.configure("TLabel", font=("Helvetica", 16))

# main_frame = Frame(root)
# main_frame.pack(pady=20, padx=20)

# instructions_label = Label(main_frame, text="Bấm'Start Listening' để bắt đầu.", font=("Helvetica", 16), pady=10)
# instructions_label.pack()

# img_label = Label(main_frame)
# img_label.pack()

# buttons_frame = Frame(main_frame)
# buttons_frame.pack(pady=10)

# start_button = ttk.Button(buttons_frame, text="Start Listening", command=lambda: start_listening(img_label))
# start_button.pack(side=tk.LEFT, padx=10)

# stop_button = ttk.Button(buttons_frame, text="Stop Listening", command=stop_listening)

# return_button = ttk.Button(buttons_frame, text="Return", command=back)
# return_button.pack(side=tk.LEFT, padx=10)

# center_window(root)

# root.mainloop()