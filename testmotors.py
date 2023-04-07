import argparse, sys

sys.path.append("..")
print(sys.path)
from blossompy import Blossom
#from anikareceive import on_message_received
import time
from time import sleep
import simpleaudio as sa
from PyQt5 import QtCore, QtGui, QtWidgets

#bl = Blossom(sequence_dir='/home/pi/src/seqeuences/woody/mina')

#bl = Blossom(sequence_dir='sequences/')

bl = Blossom(sequence_dir='sequences/')

bl.connect()


movements = {
    #order: tower_1 angle, tower_1 time, tower_2 angle, tower_2 time, tower_3 time, tower_3 angle, base angle, base time, ear angle, ear time
    "head_tilt_left": [90, 0.1, 90, 0.1, 35, 0.4, 5, 0.1,100 , 0.7],
    "head_tilt_right": [100, 0.1, 10, 0.4, 100, 0.1, 5, 0.1, 180, 0.7],
    "reset":  [100, 0.1, 100, 0.3, 100, 0.3, 0, 0.1, 100, 0.8],
    "move_ear": [100, 0.1, 100, 0.3, 100, 0.3, 5, 0.1, 400, 0.8]
    
}

def head_tilt_right():
    bl.motor_goto('tower_2', -25, 0.5)
    bl.motor_goto('tower_1', -10, 0.5)

def reset():
    bl.motor_goto('tower_1', 100, 0.5)
    bl.motor_goto('tower_3', 100, 0.5)
    bl.motor_goto('tower_2', 100, 0.5)
    bl.motor_goto('base', 0, 0.5)

def main():
        
         # safe init and connects to blossom and puts blossom in reset position
         
         for i in range(5):
             '''
             bl.motor_goto('tower_1', movements["reset"][0],movements["reset"][1])
             bl.motor_goto('tower_2', movements["reset"][2], movements["reset"][3])
             bl.motor_goto('tower_3', movements["reset"][4], movements["reset"][5])
             bl.motor_goto('base', movements["reset"][6], movements["reset"][7])
             '''
             bl.motor_goto('ears', movements["reset"][8], movements["reset"][9])


             time.sleep(1)
             
             #bl.motor_goto('tower_1', movements["head_tilt_left"][0],movements["head_tilt_left"][1])
             #bl.motor_goto('tower_2', movements["head_tilt_left"][2], movements["head_tilt_left"][3])
             #bl.motor_goto('tower_3', movements["head_tilt_left"][4], movements["head_tilt_left"][5])
             #bl.motor_goto('base', movements["head_tilt_left"][6], movements["head_tilt_left"][7])
             bl.motor_goto('ears', movements["move_ear"][8], movements["move_ear"][9])
             time.sleep(1)
             '''
             bl.motor_goto('tower_1', movements["reset"][0],movements["reset"][1])
             bl.motor_goto('tower_2', movements["reset"][2], movements["reset"][3])
             bl.motor_goto('tower_3', movements["reset"][4], movements["reset"][5])
             bl.motor_goto('ears', movements["reset"][8], movements["reset"][9])
             time.sleep(1)
             bl.motor_goto('tower_1', movements["head_tilt_right"][0],movements["head_tilt_right"][1])
             bl.motor_goto('tower_2', movements["head_tilt_right"][2], movements["head_tilt_right"][3])
             bl.motor_goto('tower_3', movements["head_tilt_right"][4], movements["head_tilt_right"][5])
             bl.motor_goto('ears', movements["head_tilt_right"][8], movements["head_tilt_right"][9])
             time.sleep(1)
             bl.motor_goto('tower_1', movements["reset"][0],movements["reset"][1])
             bl.motor_goto('tower_2', movements["reset"][2], movements["reset"][3])
             bl.motor_goto('tower_3', movements["reset"][4], movements["reset"][5])
             bl.motor_goto('ears', movements["reset"][8], movements["reset"][9])
             '''
         
         
         
         #reset()
         
         bl.load_sequences()
        #bl.do_sequence("test_head_tilt_left")
         time.sleep(2)
         print(bl.robot.get_time_sequences())
        
        #print (anikareceive.message)

if __name__ == "__main__":
    main()

