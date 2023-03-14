import argparse, sys
sys.path.append("..")
print(sys.path)
from blossompy import Blossom
from time import sleep
import random
from datetime import datetime

pause_session = False
stop_session = False

idle_sequences = ["breathing/exhale", "breathing/inhale", "fear/fear_startled", "happy/happy_lookingup", "sad/sad_downcast"]
random.shuffle(idle_sequences)

# bl = Blossom(sequence_dir='../blossompy/src/sequences', name="test")
bl = Blossom(sequence_dir='../blossompy/src/sequences', name="woody")
bl.connect() # safe init and connects to blossom and puts blossom in reset position
bl.load_sequences()

p_number = "p3"
now = datetime.now() # current date and time
date_time = now.strftime("%m/%d/%Y_%H:%M:%S")
# record_fname = date_time + p_number + ".txt"
record_fname = now.strftime('%d-%m-%Yp3.txt')
with open(record_fname, 'w') as fp:
    print('created', record_fname)
# sequence_record = open(record_fname, "x")
# sequence_record.write("Idle sequence record" + date_time + "\n")
# sequence_record.close()

def do_idle_sequence(sequence_name, f):
    print("performing " + sequence_name + "\n")
    now = datetime.now() # current date and time
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    f.write(date_time + "\n" + sequence_name + "\n")
    bl.do_sequence("reset")
    bl.do_sequence(sequence_name)

def start_idle_loop():
    print("starting idle loop \n")
    sequence_record = open(record_fname, "a")
    sequence_record.write("Start Session")
    print("wrote to start session \n")
    stop_session = False
    for sequence in idle_sequences:
        if stop_session:
            break
        else:
            print("in else block \n")
            do_idle_sequence(sequence,sequence_record)
            sleep(30)

def inhale():
    print("starting idle loop \n")
    sequence_record = open(record_fname, "a")
    sequence_record.write("Start Session")
    print("wrote to start session \n")
    stop_session = False
    for sequence in idle_sequences:
        if stop_session:
            break
        else:
            print("in else block \n")
            do_idle_sequence(sequence,sequence_record)
            sleep(30)
        
            
            







# def main(args):
#     """
#     Start robots, start up server, handle CLI
#     ToDo: the multi-robot setup should be a seperate file
#     """
#     bl = Blossom()
#     bl.connect() # safe init and connects to blossom and puts blossom in reset position

#     bl.load_sequences()

#     example_sequence = "breathing/inhale"
#     bl.do_sequence("yes")
#     sleep(5)
#     bl.do_sequence("no")
#     sleep(5)
#     bl.do_sequence("yes")
#     sleep(5)

#     bl.motor_goto("tower_2", 20)
#     bl.motor_goto("tower_3", 20)
#     sleep(2)

#     bl.motor_goto("tower_2", 80)
#     bl.motor_goto("tower_3", 80)
#     sleep(2)

#     bl.motor_goto("tower_2", 20)
#     bl.motor_goto("tower_3", 20)
#     sleep(2)

#     bl.motor_goto("tower_2", 80)
#     bl.motor_goto("tower_3", 80)
#     sleep(2)
#     # bl.motor_goto("base", 0)
#     bl.do_sequence(example_sequence)
#     sleep(2)

#     bl.cli()


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

