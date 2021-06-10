"""
Start up the blossom webserver, CLI client, and web client.
"""

# make sure that prints will be supported
from __future__ import print_function
import sys
import argparse
import os
import shutil
from src.config import RobotConfig
from src import sequencerobot
import re
import random
import time
import threading
# seed time for better randomness
random.seed(time.time())

master_robot = None
robots = []
prior_cmd, prior_args = 'rand', []

def run_cli(robot):
    """
    Handle CLI inputs indefinitely
    Will split off / or | and keep subsequent parts as a list of args
    """
    print("\nRunning CLI")
    while(1):
        # get command string
        cmd_str = input("Enter a command ('l' for a list, 'h' for help):")
        cmd_string = re.split('/| ', cmd_str)
        cmd = cmd_string[0]

        # parse to get argument
        args = None
        if (len(cmd_string) > 1):
            args = cmd_string[1:]

        # handle the command and arguments
        handle_input(master_robot, cmd, args)
    print("\nCLI Loop Exit")

def print_help():
    print(
        "Possible cmd line arguments include:" +
        "\nPlay an action:" +
        "\n\t Play a random action: rand" +
        "\n\t Play a sequence: s" +
        "\n" +
        "\nMove individual motors: m" +
        "\n" +
        "\nReload gestures from json sequences: r" +
        "\n" +
        "\nAdjust Parameters:" +
        "\n\t Adjust speed: e" +
        "\n\t Adjust amplitude: a" +
        "\n\t Adjust posture: p" +
        "\n" +
        "\nExec python command: man" +
        "\n" +
        "\nList available gestures: l or ls" +
        "\n" +
        "\nQuit: q" +
        "\n" +
        "\nEnter without a cmd to replay the last thing"
    )

def graceful_exit():
    """
    Close the robot object and clean up any temporary files.
    Manually kill the flask server because there isn't an obvious way to do so gracefully.
    """
    print("Exiting...")
    for bot in robots:
        # clean up tmp dirs and close robots
        tmp_dir = './src/sequences/%s/tmp' % bot.name
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        bot.robot.close()
    print("Bye!")

def play_sequence(cmd, robot, args):
    idle_sep = '='
    # if random, choose random sequence
    if cmd == 'rand':
        args = [random.choice(robot.seq_list.keys())]
    # default to not idling
    # idler = False
    # get sequence if not given
    if not args:
        args = ['']
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
            print(seq)
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

def print_available_sequences(args, robot):
    if args:
        args[0] = args[0].replace('*', '')
    for seq_name in robot.seq_list.keys():
        # skip if argument is not in the current sequence name
        if args and args[0] != seq_name[:len(args[0])]:
            continue
        print(seq_name)

def control_motor(args, robots):
    # get motor and pos if not given
    if not args:
        args = ['', '']
        args[0] = input('Motor: ')
        args[1] = input('Position: ')
    for bot in robots:
        if (args[0] == 'all'):
            bot.goto_position({'tower_1': float(args[1]), 'tower_2': float(
                args[1]), 'tower_3': float(args[1])}, 0, True)
        else:
            bot.goto_position({args[0]: float(args[1])}, 0, True)

def adjust_factors(cmd, robots):
    # adjust speed
    if cmd == 'e':
        for bot in robots:
            bot.speed = float(input('Choose Speed factor [range: (0.5 to 2.0)]: '))
    # adjust amplitude (0.5 to 2.0)
    elif cmd == 'a':
        for bot in robots:
            bot.amp = float(input('Choose Amplitude factor [range: (0.5 to 2.0)]: '))
    # adjust posture (-150 to 150)
    elif cmd == 'p':
        for bot in robots:
            bot.post = float(input('Choose Posture factor [range: (-150 to 150)]: '))


def handle_input(robot, cmd, args=[]):
    """
    handle CLI input

    Args:
        robot: the robot affected by the given command
        cmd: a robot command
        args: additional args for the command
    """
    global prior_cmd, prior_args

    if cmd == 's' or cmd == 'rand':
        play_sequence(cmd, robot, args)
    elif cmd == 'r':
        # reload gestures
        master_robot.load_all_sequences()
    elif cmd == 'l' or cmd == 'ls':
        print_available_sequences(args, robot)
    elif cmd == 'q':
        graceful_exit()
    elif cmd == 'm':
        control_motor(args, robots)
    elif cmd in "eap":
        adjust_factors(cmd, robots)
    elif cmd == 'h':
        print_help()
    elif cmd == '':
        handle_input(master_robot, prior_cmd, prior_args)
        return

    elif cmd in robot.seq_list.keys():
        # directly call a sequence (skip 's')
        handle_input(master_robot, 's', [cmd])
    
    elif [cmd in seq_name for seq_name in robot.seq_list.keys()]:
        # directly call a random sequence by partial name match
        if 'mix' not in cmd:
            seq_list = [seq_name for seq_name in robot.seq_list.keys() if cmd in seq_name and 'mix' not in seq_name]
        else:
            seq_list = [seq_name for seq_name in robot.seq_list.keys() if cmd in seq_name]

        if len(seq_list) == 0:
            print("No sequences matching name: %s" % (cmd))
            return
        handle_input(master_robot, 's', [random.choice(seq_list)])
        cmd = cmd

    else:
        print("Invalid input")
        return
    prior_cmd, prior_args = cmd, args



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
    t = threading.Thread(target=run_cli, args=[master_robot])
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
    return parser.parse_args(args)


"""
Generic main handler
"""
if __name__ == "__main__":
    main(parse_args(sys.argv[1:]))
