from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
import time
#from ascript import *
#import test1.py

# FOR POLLY TTS
import sys
from contextlib import closing
import boto3       # May need to install library
import pyaudio     # May need to install library
from botocore.exceptions import BotoCoreError, ClientError
from ctypes import *

# FOR ANIMATING
from blossompy import Blossom
from PyQt5 import QtCore, QtGui, QtWidgets

# For timing movements and switching between Speak and Listen states
from timeit import default_timer
import threading

# Set up AWS Polly
session = boto3.Session()
polly = session.client("polly")

# Set up audio device configurations for PyAudio
SAMPLE_RATE = 16000
READ_CHUNK = 4096
CHANNELS = 1
BYTES_PER_SAMPLE = 2

# Suppress PyAudio errors and warnings
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
    pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('libasound.so')

# Set error handler
asound.snd_lib_error_set_handler(c_error_handler)

switch = True

# Use thread Event to toggle between Speak/Listen states
speak_event = threading.Event()

# Initialize blossom
bl = Blossom(sequence_dir='sequences/')
bl.connect()  # safe init and connects to blossom and puts blossom in reset position

# Configure user topics
SUBSCRIBE_TOPIC = "pausang2211_mqtt/sub"
PUBLISH_TOPIC = "pausang2211_mqtt/pub"

# Store sequences
movements = {
    #order: tower_1 angle, tower_1 time, tower_2 angle, tower_2 time, tower_3 time, tower_3 angle, base angle, base time, ear angle, ear time
    "head_tilt_left": [100, 0.1, 100, 0.1, 35, 0.4, 5, 0.1, 100, 0.1],
    "head_tilt_right": [100, 0.1, 10, 0.4, 100, 0.1, 5, 0.1, 100, 0.1],
    "reset":  [100, 0.1, 100, 0.3, 100, 0.3, 5, 0.1, 100, 0.1],
    "move_ear": [100, 0.1, 100, 0.3, 100, 0.3, 5, 0.1, 30, 0.3]
}

# Initialize list of desired sequences and length of sequences
DESIRED_SEQUENCES = ["head_tilt_left", "reset", "head_tilt_right", "reset"]
DESIRED_SEQUENCES_TIME = {}
for seq in DESIRED_SEQUENCES:
    curr_movement = movements[seq]
    DESIRED_SEQUENCES_TIME[seq] = curr_movement[1] + curr_movement[3] + curr_movement[5] + curr_movement[7]
for seq in DESIRED_SEQUENCES_TIME:
    print("Seq_name:", seq, "\tSeq_time:", DESIRED_SEQUENCES_TIME[seq])
    
# Initialize list of idle sequences
IDLE_SEQUENCES = ["head_tilt_left", "reset"]
     
# Play sequence by name in "movements" dictionary
def play_sequence(sequence_name):
    print("Playing sequence:", sequence_name)
    bl.motor_goto('tower_1', movements[sequence_name][0],movements[sequence_name][1])
    bl.motor_goto('tower_2', movements[sequence_name][2], movements[sequence_name][3])
    bl.motor_goto('tower_3', movements[sequence_name][4], movements[sequence_name][5])
    bl.motor_goto('base', movements[sequence_name][6], movements[sequence_name][7])
    bl.motor_goto('ears', movements[sequence_name][8], movements[sequence_name][9])

# Publishing MQTT Message using the proper format onto the defined topic, PUBLISH_TOPIC
def publish_message(MESSAGE):
    data = "{}".format(MESSAGE)
    message = {"msg" : data}
    mqtt_connection.publish(topic=PUBLISH_TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
    print("Published: '" + json.dumps(message) + "' to the topic: " + "'" + PUBLISH_TOPIC + "'")

# Speaking function: uses AWS Polly for TTS and movements of Blossom motors
def on_message_received(topic, payload):
    jsonmsg = json.loads(payload.decode())
    message = jsonmsg['msg']
    print(message)
    print(type(message))
    
    # Set Speaking state to True
    speak_event.set()
    
    # Reset motor position
    play_sequence("reset")
    
    # Synthesize message using AWS Polly
    try:
        response = polly.synthesize_speech(Text=message,
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
    
    SEQ_NUM = 0      # Keep track of speaking sequence index
    
    # Speak message while also moving Blossom
    with response["AudioStream"] as polly_stream:
        play_sequence(DESIRED_SEQUENCES[SEQ_NUM])     # Play first sequence
        seq_timer_start = time.perf_counter()         # Track time that first sequence played
        audio_data = polly_stream.read(READ_CHUNK)    # Speak
        
        # As long as there is more words to speak
        while audio_data:
            seq_timer_end = time.perf_counter()       # Get current time
            
            # if the amount of time that passed since sequence played is longer than length of sequence,
            # play a new sequence
            if seq_timer_end - seq_timer_start > DESIRED_SEQUENCES_TIME[DESIRED_SEQUENCES[SEQ_NUM]]:
                SEQ_NUM = (SEQ_NUM + 1) % len(DESIRED_SEQUENCES)     # Update sequence index
                play_sequence(DESIRED_SEQUENCES[SEQ_NUM])            # Play next sequence
                seq_timer_start = time.perf_counter()                # Update time that first sequence played
                
            stream.write(audio_data)
            audio_data = polly_stream.read(READ_CHUNK)
             
    # Stop the audio and close devices
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    # Reset motor positions and let user send new message
    play_sequence("reset")
    publish_message("Done!")
    
    # Set Speaking state to False
    speak_event.clear()
    
# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a387vttjfd7bvs-ats.iot.us-west-2.amazonaws.com"
CLIENT_ID = "testDevice"
PATH_TO_CERTIFICATE = "/home/cbt-deployment/certs/certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "/home/cbt-deployment/certs/private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "/home/cbt-deployment/certs/AmazonRootCA1.pem"
MESSAGE = "Hello World"
TOPIC = "test"
RANGE = 20

# Spin up resources
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )
print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))
# Make the connect() call
connect_future = mqtt_connection.connect()
# Future.result() waits until a result is available
connect_future.result()
print("Connected!")
sub_future, packet_id = mqtt_connection.subscribe(topic=SUBSCRIBE_TOPIC,qos=mqtt.QoS.AT_LEAST_ONCE,callback=on_message_received)

sub_results = sub_future.result()

time1 = time.perf_counter()     # Start time of idle sequence
test_seq = 0                    # Track index of idle sequences
while True:
    # Listen only if it is not speaking
    if not speak_event.is_set():
        sub_results = sub_future.result()
        time2 = time.perf_counter()
        
        # If 5 seconds have passed, play next idle sequence
        if time2 - time1 > 5:
            play_sequence(IDLE_SEQUENCES[test_seq])
            test_seq = (test_seq + 1) % len(IDLE_SEQUENCES)
            time1 = time.perf_counter()
