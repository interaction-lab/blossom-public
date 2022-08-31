import argparse, sys
import pandas as pd
#import the blossom robot (basic motor ctrls)
# sys.path.insert(0,"/home/pi/blossom/src")
# import main as Blossom
#
# sys.path.insert(0,"/home/pi/blossom/src")
# from sequence import Sequence
from time import sleep

sys.path.append("..")
print(sys.path)
from blossompy import Blossom


bl = Blossom(sequence_dir='../blossompy/src/sequences')


# bl = Blossom.Blossom()
bl.connect()


def convert(radians):
  degrees = radians*(180/3.14)
  #print(degrees)
  return degrees






def main(args):
    """
    Start robots, start up server, handle CLI
    ToDo: the multi-robot setup should be a seperate file
    """

# safe init and connects to blossom and puts blossom in reset position

    #bl.load_sequences()

    # loading data from openface
    # df = pd.read_csv("webcam_2022-07-13-13-21.csv", usecols = [' timestamp', ' AU01_r', ' AU04_r', ' pose_Rx', ' pose_Ry', ' pose_Rz'])

    df = pd.read_csv("/home/interaction-lab/libraries/OpenFace/build/bin/processed/dru_test.csv", usecols = [' timestamp', ' AU01_r', ' AU04_r', ' pose_Rx', ' pose_Ry', ' pose_Rz'])

    # df[' pose_Rx'] = df[' pose_Rx'].map(lambda x:convert(x))
    # df[' pose_Ry'] = df[' pose_Ry'].map(lambda x:convert(x))
    # df[' pose_Rz'] = df[' pose_Rz'].map(lambda x:convert(x))

    # for i in range(df.shape[0]-1):
    #     turn(df.loc[i, ' pose_Ry'])
    #     UpDown(df.loc[i, ' pose_Rx'])
    #     tilt(df.loc[i, ' pose_Rz'])
    #     time(df.loc[i, ' timestamp'], df.loc[i+1, ' timestamp'])
    #     print(df.loc[i, ' pose_Rz'])
    bl.motor_goto("base", 90)
    print("Face blossom to look at you. Then look at Blossom")
    print("Press enter when you are looking at Blossom")

    string = input()
    if(string == ""):
        print("Yay")

        Position = pd.read_csv("/home/interaction-lab/libraries/OpenFace/build/bin/processed/dru_test.csv", usecols = [' pose_Rx', ' pose_Ry'])
        endLine = len(Position)-1
        Positions = [Position.loc[endLine, ' pose_Rx'], Position.loc[endLine, ' pose_Ry']]
    Min = Positions[1] - 0.2
    Max = Positions[1] + 0.2
    degrees = Positions[1]*(180/3.14)
    bl.motor_goto("base", degrees)
    while(1):
        df = pd.read_csv("/home/interaction-lab/libraries/OpenFace/build/bin/processed/dru_test.csv", usecols = [' pose_Rx', ' pose_Ry'])
        length = len(df)-1
        if(df.loc[length, ' pose_Ry'] >= Min and df.loc[length, ' pose_Ry'] <= Max):
            print("Yay")
            bl.motor_goto("base", 90)
        else:
            print("sad")
            bl.motor_goto("base", degrees)
        sleep(.1)


    bl.motor_goto("tower_2", 20)
    bl.motor_goto("tower_3", 20)
    sleep(2)

    bl.motor_goto("tower_2", 80)
    bl.motor_goto("tower_3", 80)
    sleep(2)

    bl.motor_goto("tower_2", 20)
    bl.motor_goto("tower_3", 20)
    sleep(2)

    bl.motor_goto("tower_2", 90)
    bl.motor_goto("tower_3", 90)
    bl.motor_goto("tower_1", 90)
    bl.motor_goto("base", 90)
    sleep(2)
    # bl.motor_goto("base", 0)
    #bl.do_sequence(example_sequence)
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
