import cv2
import tkinter as tk
from PIL import Image, ImageTk

class VideoApp:
    def __init__(self, window, window_title, video_path):
        self.window = window
        self.window.title(window_title)
        
        # Create a canvas to fit the video frames
        self.canvas = tk.Canvas(window)
        self.canvas.pack()

        # Set the video path directly
        self.video_path = video_path
        self.open_video()

        # Button to exit the application

    def open_video(self):
        if not self.video_path:
            return
        
        # Open the specified video file
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            print("Error: Could not open video.")
            return

        # Get video dimensions
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Set the desired scale factor (e.g., 0.5 for half size)
        self.scale_factor = 0.5
        self.new_width = int(self.width * self.scale_factor)
        self.new_height = int(self.height * self.scale_factor)

        # Update canvas size to fit the video frames
        self.canvas.config(width=self.new_width, height=self.new_height)

        # Start the video loop
        self.update_video()

    def update_video(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # Rescale frame
                frame = cv2.resize(frame, (self.new_width, self.new_height))
                # Convert frame to PIL image
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            else:
                # Loop the video
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
            self.window.after(15, self.update_video)

    def exit_app(self):
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        self.window.destroy()

# Main part of the script
if __name__ == "__main__":
    video_path = "video.MP4"  # Specify your video file path here
    root = tk.Tk()
    app = VideoApp(root, "Đáp án", video_path)
    root.mainloop()
