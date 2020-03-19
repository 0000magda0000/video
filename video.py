# Sylvia Video alters sound according to brightness in frame
from moviepy.editor import *
import numpy, scipy.io, scipy
from pydub import AudioSegment
import pydub.scipy_effects
import sys
video=sys.argv[1]
videoout=sys.argv[2]

#from scipy.io import wavfile
#from scipy import signal

print ("start")

clip = VideoFileClip(video)
print (clip.fps)
audio=clip.audio

audio.write_audiofile("test.wav")
duration = int(clip.fps * clip.duration)
print (duration)
width, height = clip.size
print (width*height*3)
audiotrack=AudioSegment.from_wav("test.wav")
audiofiles=audiotrack[0:10]

for frame_number in range (0,duration):
    frame = clip.get_frame(frame_number / clip.fps)
    brightnessValue = int(numpy.sum(frame) / (width * height * 3))
    rawvalue = brightnessValue
    crossfadevalue=10
    startpoint=int(frame_number / clip.fps * 1000)
    endpoint=int(frame_number / clip.fps * 1000+(1000/clip.fps)+crossfadevalue)
    brightnessValue=max(1000,(brightnessValue*32))
    brithtnessValue=min(15000,brightnessValue)
    print(frame_number, startpoint,endpoint,rawvalue, brightnessValue)
    filteredaudiotrack=audiotrack[startpoint:endpoint].low_pass_filter(brightnessValue)
    audiofiles=audiofiles.append(filteredaudiotrack,crossfade=crossfadevalue)

audiofiles.export("new.mp3",bitrate="128k")
audioclip=AudioFileClip("new.mp3",fps=44100)
clip2=clip.set_audio(audioclip)
clip2.write_videofile(videoout, audio=True)

#audio_codec="libmp3lame")
