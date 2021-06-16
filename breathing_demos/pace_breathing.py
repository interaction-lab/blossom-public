import argparse, sys
sys.path.append("..")
print(sys.path)
from blossompy import Blossom
from time import sleep


def main(args):
    """
    Start robots, start up server, handle CLI
    ToDo: the multi-robot setup should be a seperate file
    """
    bl = Blossom(sequence_dir='../blossompy/src/sequences')
    bl.connect() # safe init and connects to blossom and puts blossom in reset position

    bl.load_sequences()
    cmd = ""

    bl.do_sequence("reset")

    while cmd != "exit":
        cmd = input("Inpute cmd [i/e or 1-3]")
        if cmd == "i":
            #add counting 1, 2, 3
            bl.do_sequence("breathing/inhale")
            sleep(4)
        elif cmd == "e":
            bl.do_sequence("breathing/exhale")
            sleep(4)
        elif cmd == "1":
            bl.robot.speed = float(0.7)
        elif cmd == "2":
            bl.robot.speed = float(1)
        elif cmd == "3":
            bl.robot.speed = float(1.3)


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

