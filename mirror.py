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

def turn(Input):
    #print(90-Input)
    degrees =  90 - Input
    bl.motor_goto("base", degrees)

#  def tilt(Input, hight):
#     if hight <= 90:
#         if Input  >= 0:
#             Input = abs(2*Input)
#             value = hight + Input
#             bl.motor_goto("tower_3", value)
#             bl.motor_goto("tower_2", hight)
#         else:
#             Input = abs(2*Input)
#             value = hight + Input
#             bl.motor_goto("tower_2", value)
#             bl.motor_goto("tower_3", hight)
#     else:
#         if Input  >= 0:
#             Input = abs(2*Input)
#             value = hight - Input
#             bl.motor_goto("tower_2", value)
#             bl.motor_goto("tower_3", hight)
#         else:
#             Input = abs(2*Input)
#             value = hight - Input
#             bl.motor_goto("tower_3", value)
#             bl.motor_goto("tower_2", hight)

def tilt(Input):
    Input = 3*Input
    value = 60 + Input
    value2 = 60 - Input
    bl.motor_goto("tower_2", value)
    bl.motor_goto("tower_3", value2)

def UpDown(Input):
    value = -3*Input +80
    if value >= 180:
        value = 180
    if value <= 0:
        value = 0
    else:
        value = value
    bl.motor_goto("tower_1", value)
    #inverse = Inverse(value)
#    tilt(i, inverse)
def Inverse(Input):
    return 180-Input


def time(Input, NextInput):
    value = NextInput - Input
    sleep(value)

def eyebrows(Input1, Input2, Input3):
    average = (Input1 + Input2)/2
    down = 90-Input3*24
    up = 90+average*24
    if (average > Input3):
        bl.motor_goto("ears", up)
    else:
        bl.motor_goto("ears", down)


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

    while(1):
        df = pd.read_csv("/home/interaction-lab/libraries/OpenFace/build/bin/processed/dru_test.csv", usecols = [' timestamp', ' AU01_r', ' AU02_r', ' AU04_r', ' pose_Rx', ' pose_Ry', ' pose_Rz'])
        length = len(df)-1
        turn(convert(df.loc[length, ' pose_Ry']))
        UpDown(convert(df.loc[length, ' pose_Rx']))
        tilt(convert(df.loc[length, ' pose_Rz']))
        eyebrows(df.loc[length, ' AU01_r'], df.loc[length, ' AU02_r'], df.loc[length, ' AU04_r'])
        # if(df.loc[length, ' AU01_c'] == 1):
        #     bl.motor_goto("ears", 180)
        # elif(df.loc[length, ' AU04_c'] == 1):
        #     bl.motor_goto("ears", 0)
        # else:
        #     bl.motor_goto("ears", 90)
        # time(df.loc[i, ' timestamp'], df.loc[i+1, ' timestamp'])
        # print(df.loc[i, ' pose_Rz'])
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
