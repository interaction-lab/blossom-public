import argparse, sys
sys.path.append("..")
print(sys.path)
from blossompy import Blossom
from time import sleep
import simpleaudio as sa


def main(args):
    """
    Start robots, start up server, handle CLI
    ToDo: the multi-robot setup should be a seperate file
    """
    bl = Blossom(sequence_dir='../blossompy/src/sequences')
    bl.connect() # safe init and connects to blossom and puts blossom in reset position

    bl.load_sequences()
    bl.do_sequence("breathing/exhale")
    cmd = ""

    filename = "../blossompy/media/one.wav"
    wave_obj = sa.WaveObject.from_wave_file(filename)

    filename1 = "../blossompy/media/two.wav"
    wave_obj1 = sa.WaveObject.from_wave_file(filename1)

    filename2 = "../blossompy/media/three.wav"
    wave_obj2 = sa.WaveObject.from_wave_file(filename2)

    while cmd != "exit":
        cmd = input("\n\nEnter \"intro\" to play the blossom introduction."
        + "Input cmd [i/e for breath, 1-3 for speed, ci for inhale with counting or ce for exhale with counting.] or exit to exit: ")
        if cmd == "i":
            bl.do_sequence("breathing/inhale")
            sleep(3.5)
        elif cmd == "e":
            bl.do_sequence("breathing/exhale")
            sleep(3.5)
        elif cmd == "1":
            bl.robot.speed = float(0.7)
        elif cmd == "2":
            bl.robot.speed = float(1)
        elif cmd == "3":
            bl.robot.speed = float(1.3)
        elif cmd == "ci":
            bl.robot.speed = float(1)
            play_obj = wave_obj.play()
            bl.do_sequence("breathing/inhale")
            sleep(1.2)
            play_obj1 = wave_obj1.play()
            sleep(1.2)
            play_obj2 = wave_obj2.play()
            sleep(1.2)
        elif cmd == "ce":
            bl.robot.speed = float(1)
            play_obj = wave_obj.play()
            bl.do_sequence("breathing/exhale")
            sleep(1.2)
            play_obj1 = wave_obj1.play()
            sleep(1.2)
            play_obj2 = wave_obj2.play()
            sleep(1.2)
        elif cmd == "intro":
            introfile = "../blossompy/media/hi_name.wav"
            wave_obj_intro = sa.WaveObject.from_wave_file(introfile)
            play_obj = wave_obj_intro.play()
            bl.do_sequence("breathing/intermediate")
            sleep(4)
            bl.do_sequence("breathing/exhale")

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

