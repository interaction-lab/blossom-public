import argparse, sys
from blossompy import Blossom
from time import sleep


def main(args):
    """
    Start robots, start up server, handle CLI
    ToDo: the multi-robot setup should be a seperate file
    """
    bl = Blossom()
    bl.connect() # safe init and connects to blossom and puts blossom in reset position

    bl.load_sequences()

    example_sequence = "breathing/inhale"
    bl.do_sequence("yes")
    sleep(5)
    bl.do_sequence("no")
    sleep(5)
    bl.do_sequence("yes")
    sleep(5)

    bl.motor_goto("tower_2", 20)
    bl.motor_goto("tower_3", 20)
    sleep(2)

    bl.motor_goto("tower_2", 80)
    bl.motor_goto("tower_3", 80)
    sleep(2)

    bl.motor_goto("tower_2", 20)
    bl.motor_goto("tower_3", 20)
    sleep(2)

    bl.motor_goto("tower_2", 80)
    bl.motor_goto("tower_3", 80)
    sleep(2)
    # bl.motor_goto("base", 0)
    bl.do_sequence(example_sequence)
    sleep(2)

    bl.cli()


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

