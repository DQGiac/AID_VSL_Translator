import os
from pygame import mixer
import time

sound_file = "video call/sound.mp3"

# Check if the sound file exists
if os.path.isfile(sound_file):
    try:
        mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')  # Initialize it with the correct device
        mixer.music.load(sound_file)  # Load the mp3
        mixer.music.play()  # Play it

        # Wait for the music to finish playing
        while mixer.music.get_busy():
            time.sleep(1)
            
    except Exception as e:
        print(f"Error playing sound: {e}")
    
    finally:
        # Stop the music and quit the mixer
        mixer.music.stop()
        mixer.quit()
        
        # Remove the sound file
        os.remove(sound_file)
print("ok")
# Wait a short time before checking again
time.sleep(1)
