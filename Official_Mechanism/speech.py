import os
from pydub import AudioSegment
from pydub.playback import play

song = AudioSegment.from_mp3("sound.mp3")
play(song)
os.remove("sound.mp3")