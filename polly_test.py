"""Getting Started Example for Python 2.7+/3.3+"""
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
import pyaudio

# Set up audio device configurations for PyAudio
SAMPLE_RATE = 16000
READ_CHUNK = 4096
CHANNELS = 1
BYTES_PER_SAMPLE = 2

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).
session = Session(profile_name="default")
polly = session.client("polly")

# Synthesize message using AWS Polly
try:
	response = polly.synthesize_speech(Text="Hello there",
									   VoiceId="Joanna",
									   LanguageCode="en-US",
									   OutputFormat="pcm",
									   SampleRate=str(SAMPLE_RATE))
except (BotoCoreError, ClientError) as error:
	print(error)
	sys.exit(-1)

# Initialize PyAudio settings and create the audio stream
audio = pyaudio.PyAudio()
stream = audio.open(format=audio.get_format_from_width(BYTES_PER_SAMPLE),
				channels=CHANNELS,
				rate=SAMPLE_RATE,
				output=True)

# Speak message while also moving Blossom
with response["AudioStream"] as polly_stream:
	audio_data = polly_stream.read(READ_CHUNK)    # Speak
        
	# As long as there is more words to speak
	while audio_data:
		stream.write(audio_data)
		audio_data = polly_stream.read(READ_CHUNK)

# Stop the audio and close devices
stream.stop_stream()
stream.close()
audio.terminate()
