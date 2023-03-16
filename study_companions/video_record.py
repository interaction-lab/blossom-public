import cv2
import numpy as np
import pyaudio
import wave
import subprocess
from datetime import date
import datetime
import socket
import boto3
import os

#Get the rpi name
rpi_name = socket.gethostname()

# Get the current day and time of recording
time = datetime.datetime.now().strftime("%H%M")
day = date.today().strftime("%m-%d-%y")

#Naming convention for the video, auto and combined video
video_file = rpi_name + '_' + day + '_' + time +'_video.mp4'
audio_file = rpi_name + '_' + day + '_' + time + '_audio.wav'
output_file = rpi_name+ '_' + day + '_' + time +'_output.mp4'

#Set up AWS credentials and region
aws_access_key_id = 'AKIATOJSXW3AVPUR7MZJ'
aws_secret_access_key = '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'
region_name = 'us-west-2'

#Set up S3 bucket and file name
bucket_name = 'study-companions-spring-23'
video_name = output_file

# Set up audio recording parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(video_file, fourcc, 30.0, (640,480)) #Will probably need to change the fps?

# Initialize PyAudio object
audio = pyaudio.PyAudio()

# Start capturing video and audio from camera
webcam = cv2.VideoCapture(0)

# Open audio stream for recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

frames = []
num_frames = 0

# Start recording audio and video
print("Recording...")
while True:
    print("In the loop")
    ret, frame = webcam.read()
    if ret==True:
        # Write the frame to the output file
        out.write(frame)

        # Record audio
        data = stream.read(CHUNK)
        frames.append(data)

        num_frames += 1

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("We have exited the video")
            break
    else:
        break

# Stop audio stream and PyAudio object
stream.stop_stream()
stream.close()
audio.terminate()

# Release resources
webcam.release()
out.release()
cv2.destroyAllWindows()

# Save audio to WAV file
with wave.open(audio_file, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print("We are combining the audio and video files")
print("We will create an S3 client")
# Create an S3 client
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key,
                  region_name=region_name)

# Combine the audio and video files into a single mp4 file
cmd = f'ffmpeg -i {video_file} -i {audio_file} -c:v copy -c:a aac -strict experimental -shortest {output_file}'
print("We've combined the files")
# Upload the combined video file to S3
subprocess.call(cmd, shell=True)

try:
    print("We are uploading this")
    s3.upload_file(video_name, bucket_name, rpi_name + "/" + day + "/" + output_file)
    print('Complete video uploaded successfully')
    s3.upload_file(audio_file, bucket_name, rpi_name + "/" + day + "/" + audio_file)
    print('Audio uploaded successfully')
    s3.upload_file(video_file, bucket_name, rpi_name + "/" + day + "/" + video_file)
    print("Video uploaded successfully")
except Exception as e:
    print("This has failed")
    print(f'Error uploading video: {str(e)}')
print("We have called subprocess")



