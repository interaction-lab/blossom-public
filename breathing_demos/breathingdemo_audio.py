# make sure that prints will be supported
import argparse, sys
import random
import time
sys.path.append("..")
print(sys.path)
from blossompy import Blossom
from time import sleep
import simpleaudio as sa #used for playing audio files to facilitate exercise
# seed time for better randomness
random.seed(time.time())

master_robot = None
robots = []
last_cmd, last_args = 'rand', []


def main(args):

    bl = Blossom(sequence_dir='../blossompy/src/sequences')
    bl.connect() # safe init and connects to blossom and puts blossom in reset position

    bl.load_sequences()

    bl.do_sequence("breathing/startbreath")
    time.sleep(4)

    filename = "../blossompy/media/breathing_facilitation.wav"
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    print("\nplaying audio\n")
    time.sleep(27)

    for i in range (0,2):
        # get command string
        print("\ninhaling . . .\n")
        bl.do_sequence("breathing/inhale")
        time.sleep(5)
        print("\nexhaling . . .\n")
        bl.do_sequence("breathing/exhale")
        time.sleep(4)
        # parse to get argument

    bl.do_sequence("breathing/intermediate")
    time.sleep(27)
    bl.do_sequence("breathing/startbreath")

    for i in range (0,2):
        # get command string
        print("\ninhaling . . .\n")
        bl.do_sequence("breathing/inhale")
        time.sleep(5)
        print("\nexhaling . . .\n")
        bl.do_sequence("breathing/exhale")
        time.sleep(5)

    bl.do_sequence("breathing/intermediate")
    time.sleep(20)
    bl.do_sequence("breathing/startbreath")
    time.sleep(3)

    for i in range (0,3):
        # get command string
        print("\ninhaling . . .\n")
        bl.do_sequence("breathing/inhale")
        time.sleep(6.5)
        print("\nexhaling . . .\n")
        bl.do_sequence("breathing/exhale")
        time.sleep(4.5)

    print("\nFinished! Thanks for trying Blossom Breathing.")
        # handle the command and arguments

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
