from flask import Flask
from flask import render_template
from importlib import import_module
from flask_socketio import SocketIO
from engineio.payload import Payload
import sys
import os
import json
import subprocess

app = Flask(__name__)
socketio = SocketIO(app, ping_timeout=600, ping_interval=5)
Payload.max_decode_packets = 50

#import the blossom robot (basic motor ctrls)
sys.path.insert(0,"/home/pi/blossom-public")
# import main as Blossom
from blossompy import Blossom

#sys.path.insert(0,"/home/pi/blossom-public/blossompy/src")
#from sequence import Sequence

# @app.route('/favicon.ico') 
# def favicon(): 
#     return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
  return render_template("index.html")

@socketio.on('connect')
def connect():

	print("client connected")
	global robot
	print("initializing robot")
#	robot = Blossom.Blossom()
#	robot.connect() #safe init the robot to reset position
	robot = Blossom(sequence_dir='/home/pi/blossom-public/blossompy/src/sequences')
	robot.connect() # safe init and connects to blossom and puts blossom in reset position

	#load sequences from directory
	print("loading sequences...")
	robot.load_sequences()
	seq_list = list(robot.robot.seq_list.keys())
	socketio.emit('get_seq_list',json.dumps(seq_list))

	#init new list of frames
	global frames_list
	frames_list = []
	print("robot complete")

@socketio.on('disconnect')
def disconnect():
	print("client has disconnected")
	global robot
	robot.reset()
	print("blossom returned to reset position")
	robot.quit() #remove all temporary directories
	print("pypot robot deleted")

@socketio.on('record_sequence')
def record_sequence(input):
	global frames_list
	frames_list.append(input)

@socketio.on('stop_sequence')
def stop_sequence(input):
	seq_name = input['sequence_name']

	#create json object/python dict
	global frames_list
	robot_dir = "/home/pi/blossom-public/blossompy/src/sequences/" + robot.name + "/"
	seq_fn = robot_dir + seq_name + '_sequence.json'
	with open(seq_fn,'w') as seq_file:
		json.dump({'animation': seq_name, 'frame_list': frames_list[:-15]}, seq_file, indent=2)

	#add the sequence to list
	seq = Sequence.from_json(seq_fn,True)
	robot.robot.add_sequence(seq)

	#reset the frame_list
	frames_list = []
	print("sequence successfully saved")

@socketio.on('save_playback')
def save_playback(input):
	seq_name = input['sequence_name']

	robot_dir = "/home/pi/blossom-public/blossompy/src/sequences/" + robot.name + "/"
	seq_fn = robot_dir + seq_name + '_sequence.json'
	with open(seq_fn,'w') as seq_file:
		json.dump({'animation': seq_name, 'frame_list': input['frame_list']}, seq_file, indent=2)

	#add the sequence to list
	seq = Sequence.from_json(seq_fn,True)
	robot.robot.add_sequence(seq)
	print("playback successfully saved")

@socketio.on('retrieve_seq_file')
def retrieve_seq_file(input):
	print("retrieving file")
	seq_name = input['sequence_name']

	#retrieve the json file
	robot_dir = "/home/pi/blossom-public/blossompy/src/sequences/" + robot.name + "/"
	seq_file = open(robot_dir + seq_name + '_sequence.json', 'r')
	data = json.load(seq_file)
	socketio.emit('get_seq_file',data)

@socketio.on('move_robot')
def move_robot(input):
	print("moving robot")
	global robot
	robot.robot.goto_position(input)

@socketio.on('play_sequence')
def play_sequence(input):
	global robot
	seq = robot.do_sequence(input['sequence_name'])
	print("blossom complete sequence")

@socketio.on('update_motor')
def update_motor(motor_name,position):
	global robot
	robot.motor_goto(motor_name,position)
	print("motor has updated")

if __name__ == '__main__':
    app.run(host='10.25.17.223', port=5000) #insert the ip address of the raspberry pi

