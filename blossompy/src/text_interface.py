from __future__ import print_function
import sys, os, re
import argparse, shutil
from .config import RobotConfig
from .sequencerobot import SequenceRobot
import random, time
import threading
from getch import getch, pause
import json
import yaml
#with open(r'..constants.yaml') as file:
    #constants = yaml.load(file, Loader=yaml.FullLoader)

# seed time for better randomness
random.seed(time.time())


class CLI():
    def __init__(self, robot):
        self.robot = robot
        self.prior_cmd, self.prior_args = 'rand', []
        self.help_text = ("Possible cmd line arguments include:" +
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
            "\n\t Create a new configuration: c" +
            "\n" +
            "\nExec python command: man" +
            "\n" +
            "\nList available gestures: l or ls" +
            "\n" +
            "\nQuit: q" +
            "\n" +
            "\nEnter without a cmd to replay the last thing"
        )

    def print_help(self):
        print(self.help_text)

    def run_cli(self):
        """
        Handle CLI inputs indefinitely
        Will split off / or | and keep subsequent parts as a list of args
        """
        print("\nRunning CLI")
        while(1):
            # get command string
            cmd_str = input("Enter a command ('l' for a list, 'h' for help):")
            if cmd_str =="exit": break
            cmd_string = re.split('/| ', cmd_str)
            cmd = cmd_string[0]

            # parse to get argument
            args = None
            if (len(cmd_string) > 1):
                args = cmd_string[1:]

            # handle the command and arguments
            self.handle_input(cmd, args)
        print("\nCLI Loop Exit")

    def handle_input(self, cmd, args=[]):
        """
        handle CLI input

        Args:
            robot: the robot affected by the given command
            cmd: a robot command
            args: additional args for the command
        """

        if cmd == 's' or cmd == 'rand':
            self.play_sequence(cmd, args)
        elif cmd == 'r':
            # reload gestures
            self.robot.load_all_sequences()
        elif cmd == 'l' or cmd == 'ls':
            self.print_available_sequences(args)
        elif cmd == 'q':
            self.graceful_exit()
        elif cmd == 'm':
            self.control_motor(args)
        elif cmd == 'e':
            self.robot.speed = float(input('Choose Speed factor [range: (0.5 to 2.0)]: '))
        elif cmd == 'a':
            self.robot.amp = float(input('Choose Amplitude factor [range: (0.5 to 2.0)]: '))
        elif cmd == 'p':
            self.robot.post = float(input('Choose Posture factor [range: (-150 to 150)]: '))
        elif cmd == 'h':
            self.print_help()
        elif cmd == 'c':
            all_pos = []
            new_sequence = input('Please enter the name of sequence you would like to create.')
            new_cmd = self.change_motors()
            while(new_cmd != 's'):
                new_cmd = self.change_motors()
                if(new_cmd == 's'):
                    new_cmd = input("\nEnter s to save this as your final sequence." + 
                    "Enter p to add another position to this sequence.")
                    new_pos = [{'dof':key,"pos":value} for key,value in self.robot.get_motor_pos().items()]
                    all_pos.append({"positions":new_pos, "millis": 3000})
            self.write_position_to_json(all_pos, new_sequence)
        elif cmd == '':
            self.handle_input(self.prior_cmd, self.prior_args)
            return
        elif cmd in self.robot.seq_list.keys():
            # directly call a sequence (skip 's')
            self.handle_input('s', [cmd])
        elif [cmd in seq_name for seq_name in self.robot.seq_list.keys()]:
            # directly call a random sequence by partial name match
            if 'mix' not in cmd:
                seq_list = [seq_name for seq_name in self.robot.seq_list.keys() if cmd in seq_name and 'mix' not in seq_name]
            else:
                seq_list = [seq_name for seq_name in self.robot.seq_list.keys() if cmd in seq_name]
            if len(seq_list) == 0:
                print("No sequences matching name: %s" % (cmd))
                return
            self.handle_input('s', [random.choice(seq_list)])
            cmd = cmd
        else:
            print("Invalid input")
            return
        self.prior_cmd, self.prior_args = cmd, args

    def play_sequence(self, cmd, args):
        print("Playing Sequence: ", cmd, args)
        idle_sep = '='
        # if random, choose random sequence
        if cmd == 'rand':
            args = [random.choice(self.robot.seq_list.keys())]
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
        if seq in self.robot.seq_list:
            # print("Playing sequence: %s"%(args[0]))
            # iterate through all robots
            if not self.robot.seq_stop:
                self.robot.seq_stop = threading.Event()
            self.robot.seq_stop.set()
            print(seq)
            seq_thread = self.robot.play_recording(seq, idler=False)
            # go into idler
            if (idle_seq != ''):
                while (seq_thread.is_alive()):
                    # sleep necessary to smooth motion
                    time.sleep(0.1)
                    continue
                if not self.robot.seq_stop:
                    self.robot.seq_stop = threading.Event()
                self.robot.seq_stop.set()
                self.robot.play_recording(idle_seq, idler=True)
        # sequence not found
        else:
            print("Unknown sequence name:", seq)
            return

    def print_available_sequences(self, args):
        if args:
            args[0] = args[0].replace('*', '')
        for seq_name in self.robot.seq_list.keys():
            # skip if argument is not in the current sequence name
            if args and args[0] != seq_name[:len(args[0])]:
                continue
            print(seq_name)

    def graceful_exit(self):
        """
        Close the robot object and clean up any temporary files.
        Manually kill the flask server because there isn't an obvious way to do so gracefully.
        """

        # clean up tmp dirs and close robots
        tmp_dir = './src/sequences/%s/tmp' % self.robot.name
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        self.robot.robot.close()
        print("Bye!")

    def control_motor(self, args):
        # get motor and pos if not given
        if not args:
            args = ['', '']
            args[0] = input('Motor: ')
            args[1] = input('Position: ')
        if (args[0] == 'all'):
            self.robot.goto_position({'tower_1': float(args[1]), 'tower_2': float(
                args[1]), 'tower_3': float(args[1])}, 0, True)
        else:
            self.robot.goto_position({args[0]: float(args[1])}, 0, True)
    
    #allows the user to change the position of the robot using arrow keys. command is c
    def change_motors(self):
        moving_motor = input("Enter a motor ID to shift the motor (1, 2, 3, or 4). Press e to end: ")
        while(moving_motor != 'e'):
            #if one of the tower motors is being controlled
            if(int(moving_motor) > 0 and int(moving_motor) < 4):
                tower = 'tower_' + str(moving_motor)
                print("\n\nUse the up/down arrow keys to move motor " + moving_motor +
                    ".\nHit esc to stop moving the motor.\n\n")
                key = ord(getch())
                if(key == 27):
                    getch()
                    key = ord(getch())
                    if(key == 65):
                        current_pos = self.robot.get_indiv_motor_pos(tower)
                        if(current_pos < 140):
                            self.robot.goto_position({tower: float(current_pos+20)}, 0, True)
                        else:
                            self.robot.goto_position({tower: float(150)}, 0, True)
                    elif(key == 66):
                        current_pos = self.robot.get_indiv_motor_pos(tower)
                        if(current_pos > -140):
                            self.robot.goto_position({tower: float(current_pos-20)}, 0, True)
                        else:
                            self.robot.goto_position({tower: float(-150)}, 0, True)
                    elif(key == 27):
                        moving_motor = 'esc'
                if(key == 101):
                    moving_motor = 'e'
        to_return = input("Press s to save your motor configuration, or m to move another motor: ")
        return to_return
        #return #str that determines if user is moving more motors or if user is saving motor config
    
    #allows user to save the robots current position to a json file
    def write_position_to_json(self, all_pos, new_sequence):
        new_sequence = new_sequence + "_sequence.json"
        data = {"animation":new_sequence, "frame_list": all_pos}
        json_str = json.dumps(data, indent=4)
        print(json_str)
        target_path = 'src/sequences/woody/'
        if not os.path.exists(target_path):
            try:
               os.makedirs(target_path)
            except Exception as e:
                print(e)
                raise
        with open(os.path.join(target_path, new_sequence), 'w') as f:
            json.dump(data, f)
    

# def main(args):
#     """
#     Start robots, start up server, handle CLI
#     ToDo: the multi-robot setup should be a seperate file
#     """
#     # get robots to start

#     # use first name as master
#     configs = RobotConfig().get_configs(args.names)
#     master_robot = SequenceRobot(args.names[0], configs[args.names[0]])
#     configs.pop(args.names[0])

#     master_robot.reset_position()

#     # start CLI
#     cli = CLI(master_robot)
#     t = threading.Thread(target=cli.run_cli)
#     t.daemon = True
#     t.start()

#     while True:
#         time.sleep(1)


# def parse_args(args):
#     """
#     Parse arguments from starting in terminal
#     args:
#         args    the arguments from terminal
#     returns:
#         parsed arguments
#     """
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--names', '-n', type=str, nargs='+',
#                         help='Name of the robot.', default=["woody"])
#     return parser.parse_args(args)


# """
# Generic main handler
# """
# if __name__ == "__main__":
#     main(parse_args(sys.argv[1:]))
