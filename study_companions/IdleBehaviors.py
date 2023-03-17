import argparse, sys
sys.path.append("..")
from blossompy import Blossom
from time import sleep
import random

from log_session import SessionLogger

class BlossomController():
    def __init__(self):
        self.do_idle = False
        self.bl = Blossom(name="woody")
        self.bl.connect()

        self.logger = SessionLogger("blossom_behavior_log_")

        self.gaze_interval = [15,22]
        self.next_gaze = random.randint(self.gaze_interval[0],self.gaze_interval[1])
        self.ps_interval = [20,30]
        self.next_ps = random.randint(self.ps_interval[0],self.ps_interval[1])
        self.next_sigh = 60

    def sigh(self):
        self.logger.log_event("sigh")
        self.bl.motor_goto("all", 90, 1.0)
        sleep(2)
        self.bl.motor_goto("all", 0, 1.0)
        self.next_sigh = 60

    def idle_gaze(self):
        base_position = random.choice([-45, 0, 45])
        tower_1_position = random.choice([-90, 0, 90])
        self.logger.log_event("idle_gaze base " + str(base_position) + " tower_1 " + str(tower_1_position))
        self.bl.motor_goto('base', base_position, 1.0)
        self.bl.motor_goto('tower_1', tower_1_position, 1.0)
        self.next_gaze = random.randint(self.gaze_interval[0],self.gaze_interval[1])

    def posture_sway(self):
        sway_position = random.randrange(3)
        self.logger.log_event("posture sway, position " + str(sway_position))
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
        self.next_ps = random.randint(self.ps_interval[0],self.ps_interval[1])
    
    def countdown(self):
        self.next_gaze -= 1
        self.next_ps -= 1
        self.next_sigh -= 1
        if self.next_sigh<=0:
            self.sigh()
        if self.next_gaze<=0:
            self.idle_gaze()
        if self.next_ps<=0:
            self.posture_sway()

    def reset(self):
        self.logger.log_event("reset")
        self.bl.motor_goto('tower_1', 100, 0.5)
        self.bl.motor_goto('tower_2', 100, 0.5)
        self.bl.motor_goto('tower_3', 100, 0.5)
        self.bl.motor_goto('base', 0, 0.5)

    def disconnect(self):
        self.reset()
        self.logger.
