"""
Start up the blossom breathing demo with the CLI client.
Uses demo video from teachers at the Pacific Autism Center for Education.
"""

# make sure that prints will be supported
from __future__ import print_function
import sys
import yaml
import argparse
import string
import os
import shutil
import signal
from src.config import RobotConfig
from src import robot, sequence
from src import sequencerobot
import re
from serial.serialutil import SerialException
from pypot.dynamixel.controller import DxlError
import random
import cv2
import numpy as np
import time
import threading
import uuid
import requests
# seed time for better randomness
random.seed(time.time())

master_robot = None
robots = []

'''
CLI Code
'''


def start_cli(robot):
    """
    Start CLI as a thread
    """
    t = threading.Thread(target=run_cli, args=[master_robot])
    t.daemon = True
    t.start()
    cap = cv2.VideoCapture('PACETeacherDemo.mov')

    time.sleep(5)

    while(cap.isOpened()):
        ret, frame = cap.read()

        cv2.imshow('frame', frame);
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def run_cli(robot):
    """
    Handle CLI inputs indefinitely
    """

    cmd = 's';
    args = ["reset"];
    handle_input(master_robot, cmd, args)
    time.sleep(3);

    for i in range (0,10):
        # get command string
        args = ["breathing/inhale"];
        handle_input(master_robot, cmd, args)
        time.sleep(5);
        args = ['breathing/exhale'];
        handle_input(master_robot, cmd, args)

    print("\nFinished! Thanks for trying Blossom Breathing.")
        # handle the command and arguments

def handle_quit():
    """
    Close the robot object and clean up any temporary files.
    Manually kill the flask server because there isn't an obvious way to do so gracefully.

    Raises:
        ???: Occurs when yarn failed to start but yarn_process was still set to true.
    """
    print("Exiting...")
    for bot in robots:
        # clean up tmp dirs and close robots
        tmp_dir = './src/sequences/%s/tmp' % bot.name
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        bot.robot.close()
    print("Bye!")
    # TODO: Figure out how to kill flask gracefully


last_cmd, last_args = 'rand', []


def handle_input(robot, cmd, args=[]):
    """
    handle CLI input

    Args:
        robot: the robot affected by the given command
        cmd: a robot command
        args: additional args for the command
    """
    # manipulate the global speed and amplitude vars
    # global speed
    # global amp
    # global post
    # print(cmd, args)
    # separator between sequence and idler
    global last_cmd, last_args
    idle_sep = '='
    # play sequence

    for bot in robots:
        bot.speed = float(2);

    if cmd == 's' or cmd == 'rand':
        # if random, choose random sequence
        if cmd == 'rand':
            args = [random.choice(robot.seq_list.keys())]
        # default to not idling
        # idler = False
        # get sequence if not given
        if not args:
            args = ['']
            # args[0] = raw_input('Sequence: ')
            seq = input('Sequence: ')
        else:
            seq = args[0]
        # check if should be idler
        # elif (args[0] == 'idle'):
        #     args[0] = args[1]
        #     idler = True
        idle_seq = ''
        if (idle_sep in seq):
            (seq, idle_seq) = re.split(idle_sep + '| ', seq)

        # catch hardcoded idle sequences
        if(seq == 'random'):
            random.seed(time.time())
            seq = random.choice(['calm', 'slowlook', 'sideside'])
        if(idle_seq == 'random'):
            random.seed(time.time())
            idle_seq = random.choice(['calm', 'slowlook', 'sideside'])
        if (seq == 'calm' or seq == 'slowlook' or seq == 'sideside'):
            idle_seq = seq

        # play the sequence if it exists
        if seq in robot.seq_list:
            # print("Playing sequence: %s"%(args[0]))
            # iterate through all robots
            for bot in robots:
                if not bot.seq_stop:
                    bot.seq_stop = threading.Event()
                bot.seq_stop.set()
                seq_thread = bot.play_recording(seq, idler=False)
            # go into idler
            if (idle_seq != ''):
                while (seq_thread.is_alive()):
                    # sleep necessary to smooth motion
                    time.sleep(0.1)
                    continue
                for bot in robots:
                    if not bot.seq_stop:
                        bot.seq_stop = threading.Event()
                    bot.seq_stop.set()
                    bot.play_recording(idle_seq, idler=True)
        # sequence not found
        else:
            print("Unknown sequence name:", seq)
            return
    else:
        print("Invalid input")
        return
    last_cmd, last_args = cmd, args

def record(robot):
    """
    Start new recording session on the robot
    """
    # stop recording if one is happening
    if not robot.rec_stop:
        robot.rec_stop = threading.Event()
    # start recording thread
    robot.rec_stop.set()
    robot.start_recording()


def stop_record(robot, seq_name=""):
    """
    Stop recording
    args:
        robot       the robot under which to save the sequence
        seq_name    the name of the sequence
    returns:
        the name of the saved sequence
    """
    # stop recording
    robot.rec_stop.set()

    # if provided, save sequence name
    if seq_name:
        seq = robot.rec_thread.save_rec(seq_name, robots=robots)
        store_gesture(seq_name, seq)
    # otherwise, give it ranodm remporary name
    else:
        seq_name = uuid.uuid4().hex
        robot.rec_thread.save_rec(seq_name, robots=robots, tmp=True)

    # return name of saved sequence
    return seq_name


def store_gesture(name, sequence, label=""):
    """
    Save a sequence to GCP datastore
    args:
        name: the name of the sequence
        sequence: the sequence dict
        label: a label for the sequence
    """
    url = "https://classification-service-dot-blossom-gestures.appspot.com/gesture"
    payload = {
        "name": name,
        "sequence": sequence,
        "label": label,
    }
    requests.post(url, json=payload)


'''
Main Code
'''


def main(args):
    """
    Start robots, start up server, handle CLI
    """
    # get robots to start
    global master_robot
    global robots

    # use first name as master
    configs = RobotConfig().get_configs(args.names)
    print(configs)
    master_robot = safe_init_robot(args.names[0], configs[args.names[0]])
    configs.pop(args.names[0])
    # start robots
    robots = [safe_init_robot(name, config)
              for name, config in configs.items()]
    robots.append(master_robot)

    master_robot.reset_position()

    # start CLI
    start_cli(master_robot)
    while True:
        time.sleep(1)



def safe_init_robot(name, config):
    """
    Safely start/init robots, due to sometimes failing to start motors
    args:
        name    name of the robot to start
        config  the motor configuration of the robot
    returns:
        the started SequenceRobot object
    """
    # SequenceRobot
    bot = None
    # limit of number of attempts
    attempts = 10

    # keep trying until number of attempts reached
    while bot is None:
        try:
            bot = sequencerobot.SequenceRobot(name, config)
        except (DxlError, NotImplementedError, RuntimeError, SerialException) as e:
            if attempts <= 0:
                raise e
            print(e, "retrying...")
            attempts -= 1
    return bot


def parse_args(args):
    """
    Parse arguments from starting in terminal
    args:
        args    the arguments from terminal
    returns:
        parsed arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--names', '-n', type=str, nargs='+',
                        help='Name of the robot.', default=["woody"])
    parser.add_argument('--port', '-p', type=int,
                        help='Port to start server on.', default=8000)
    # parser.add_argument('--host', '-i', type=str, help='IP address of webserver',
    #                     default=srvr.get_ip_address())
    parser.add_argument('--browser-disable', '-b',
                        help='prevent a browser window from opening with the blossom UI',
                        action='store_true')
    parser.add_argument('--list-robots', '-l',
                        help='list all robot names', action='store_true')
    return parser.parse_args(args)


"""
Generic main handler
"""
if __name__ == "__main__":
    main(parse_args(sys.argv[1:]))
