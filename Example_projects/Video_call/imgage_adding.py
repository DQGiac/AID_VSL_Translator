import cv2
import pyvirtualcam
import os
import time
import numpy as np

# Function to open a camera with error handling
def open_camera(index=0):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"Cannot open camera with index {index}")
        return None
    return cap

# Function to open a video with error handling
def open_video(path):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print(f"Cannot open video at {path}")
        return None
    return cap

# Function to get the last modified time of a file
def get_modified_time(path):
    return os.path.getmtime(path)

# Path to the video to be overlayed
video_path = r"C:\Users\TechCare\Desktop\ai python\video call\video.mp4"  # Change the path accordingly

# Open the physical camera
cap = open_camera()
if cap is None:
    exit()

# Check the frame size from the physical camera
ret, frame = cap.read()
if not ret:
    print("Cannot read frame from webcam")
    cap.release()
    exit()

# Get initial modification time of the video file
last_modified_time = get_modified_time(video_path)

# Function to process the video and overlay it on the webcam feed
def process_video(video_path, cap, cam):
    overlay_cap = open_video(video_path)
    if overlay_cap is None:
        cap.release()
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Cannot read frame from webcam")
            break

        # Check if the video file has been modified
        current_modified_time = get_modified_time(video_path)
        if current_modified_time != last_modified_time:
            print("Video file has been modified, reloading...")
            overlay_cap.release()
            return current_modified_time

        # Read the next frame from the overlay video
        ret_overlay, overlay_frame = overlay_cap.read()
        if not ret_overlay:
            overlay_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Rewind to the start if video ends
            ret_overlay, overlay_frame = overlay_cap.read()
            if not ret_overlay:
                print("Cannot read frame from video")
                break

        # Check if the overlay frame is not black
        if np.sum(overlay_frame) > 0:
            # Resize overlay_frame to be smaller than the main frame
            overlay_frame_resized = cv2.resize(overlay_frame, (frame.shape[1] // 3, frame.shape[0] // 3))

            # Insert the video frame into the bottom right corner of the main frame
            overlay_h, overlay_w = overlay_frame_resized.shape[:2]
            frame[-overlay_h:, -overlay_w:] = overlay_frame_resized[:, :, :3]  # Use only the first 3 color channels (BGR)

        # Convert frame from BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Send the frame with overlay to the virtual camera
        cam.send(frame_rgb)

        # Wait until the next frame
        cam.sleep_until_next_frame()

        # Display the frame (optional)
        cv2.imshow('frame', frame)

        # Exit by pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    overlay_cap.release()
    return current_modified_time

# Start the virtual camera
with pyvirtualcam.Camera(width=frame.shape[1], height=frame.shape[0], fps=20) as cam:
    print(f'Using virtual camera: {cam.device}')

    while True:
        last_modified_time = process_video(video_path, cap, cam)

        # Add a short delay to avoid constant polling
        time.sleep(1)

cap.release()
cv2.destroyAllWindows()
