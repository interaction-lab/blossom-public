import argparse, sys
sys.path.append("..")
from blossompy import Blossom
from time import sleep
import random

class BlossomController():
    def __init__(self):
        self.do_idle = False
        self.bl = Blossom(name="woody")
        self.bl.connect()

    def sigh(self):
        self.bl.motor_goto("all", 90, 1.0)
        sleep(2)
        self.bl.motor_goto("all", 0, 1.0)

    def idle_gaze(self):
        base_position = random.choice([-45, 0, 45])
        tower_1_position = random.choice([-90, 0, 90])
        self.bl.motor_goto('base', base_position, 1.0)
        self.bl.motor_goto('tower_1', tower_1_position, 1.0)

    def posture_sway(self):
        sway_position = random.randrange(3)
        self.bl.motor_goto('tower_1', 0, 0.5)
        if sway_position == 0:
            self.bl.motor_goto('tower_2', -45, 1.0)
            self.bl.motor_goto('tower_3', 180, 1.0)
        elif sway_position == 1:
            self.bl.motor_goto('tower_2', 180, 1.0)
            self.bl.motor_goto('tower_3', -45, 1.0)
        elif sway_position == 2:
            self.bl.motor_goto('tower_2', 0, 1.0)
            self.bl.motor_goto('tower_3', 0, 1.0)

    def reset(self):
        self.bl.motor_goto('tower_1', 100, 0.5)
        self.bl.motor_goto('tower_2', 100, 0.5)
        self.bl.motor_goto('tower_3', 100, 0.5)
        self.bl.motor_goto('base', 0, 0.5)

    def disconnect(self):
        self.reset()