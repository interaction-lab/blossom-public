"""
Start up the blossom webserver, CLI client, and web client.
"""

# make sure that prints will be supported
from __future__ import print_function
import sys
import argparse
from src.config import RobotConfig
from src import sequencerobot
import random
import time
import threading
from start import *
import simpleaudio as sa #used for playing audio files to facilitate exercise
# seed time for better randomness
random.seed(time.time())

master_robot = None
robots = []
last_cmd, last_args = 'rand', []


def run_demo(robot):
    """
    Handle CLI inputs indefinitely
    """
    cmd = 's'
    args = ["breathing/startbreath"]
    handle_input(master_robot, cmd, args)
    time.sleep(4)

    filename = 'media/breathing_facilitation.wav'
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    print("\nplaying\n")
    time.sleep(2)

    for i in range (0,2):
        # get command string
        args = ["breathing/inhale"]
        print("\ninhaling . . .\n")
        handle_input(master_robot, cmd, args)
        time.sleep(5)
        args = ['breathing/exhale']
        print("\nexhaling . . .\n")
        handle_input(master_robot, cmd, args)
        time.sleep(4)
        # parse to get argument

    args = ["breathing/intermediate"]
    handle_input(master_robot, cmd, args)
    time.sleep(27)
    args = ["breathing/startbreath"]
    handle_input(master_robot, cmd, args)

    for i in range (0,2):
        # get command string
        args = ["breathing/inhale"]
        print("\ninhaling . . .\n")
        handle_input(master_robot, cmd, args)
        time.sleep(5)
        args = ['breathing/exhale']
        print("\nexhaling . . .\n")
        handle_input(master_robot, cmd, args)
        time.sleep(5)

    args = ["breathing/intermediate"]
    handle_input(master_robot, cmd, args)
    time.sleep(20)
    args = ["breathing/startbreath"]
    handle_input(master_robot, cmd, args)
    time.sleep(3)

    for i in range (0,3):
        # get command string
        args = ["breathing/inhale"]
        print("\ninhaling . . .\n")
        handle_input(master_robot, cmd, args)
        time.sleep(5)
        args = ['breathing/exhale']
        print("\nexhaling . . .\n")
        handle_input(master_robot, cmd, args)
        time.sleep(4.5)

    print("\nFinished! Thanks for trying Blossom Breathing.")
        # handle the command and arguments


def main(args):
    """
    Start robots, start up server, handle CLI
    ToDo: the multi-robot setup should be a seperate file
    """
    # get robots to start
    global master_robot
    global robots

    # use first name as master
    configs = RobotConfig().get_configs(args.names)
    master_robot = sequencerobot.SequenceRobot(args.names[0], configs[args.names[0]])
    configs.pop(args.names[0])

    # start robots
    robots = [sequencerobot.SequenceRobot(name, config)
              for name, config in configs.items()]
    print("Running with # robots: ", len(robots))
    robots.append(master_robot)

    master_robot.reset_position()

    # start CLI
    t = threading.Thread(target=run_demo, args=[master_robot])
    t.daemon = True
    t.start()

    while True:
        time.sleep(1)


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
