import argparse, sys
from blossompy import Blossom
from time import sleep
import random
import sched

class Idle():
    def __init__(self, bl):
        self.do_idle = False

    def start(self):
        self.do_idle = True
        sc = sched.scheduler()
        while self.do_idle:
            sc.enter(60, 1, sigh, (sc,))
            sc.enter(20, 1, idle_gaze, (sc,))
            sc.enter(25, 1, posture_sway, (sc,))
            sc.run()
    
    def end(self):
        self.do_idle = False

    def sigh(sc):
        bl.motor_goto("all", 90, 1.0)
        sleep(2)
        bl.motor_goto("all", 0, 1.0)

    def idle_gaze(sc):
        base_position = random.choice([-45, 0, 45])
        tower_1_position = random.choice([-90, 0, 90])
        bl.motor_goto('base', base_position, 0.5)
        bl.motor_goto('tower_1', tower_1_position, 0.5)

    def posture_sway(sc):
        sway_position = random.randrange(3)
        bl.motor_goto('tower_1', 0, 0.5)
        if sway_position == 0:
            bl.motor_goto('tower_2', -45, 0.5)
            bl.motor_goto('tower_3', 180, 0.5)
        elif sway_position == 1:
            bl.motor_goto('tower_2', 180, 0.5)
            bl.motor_goto('tower_3', -45, 0.5)
        elif sway_position == 2:
            bl.motor_goto('tower_2', 0, 0.5)
            bl.motor_goto('tower_3', 0, 0.5)


############################################
bl = Blossom()

def main():
    """
    Start robots, start up server, handle CLI
    ToDo: the multi-robot setup should be a seperate file
    """
    bl.connect() # safe init and connects to blossom and puts blossom in reset position

    sc = sched.scheduler()
    while 1:
        sc.enter(60, 1, sigh, (sc,))
        sc.enter(20, 1, idle_gaze, (sc,))
        sc.enter(25, 1, posture_sway, (sc,))
        sc.run()
    

def sigh(sc):
    bl.motor_goto("all", 90, 1.0)
    sleep(2)
    bl.motor_goto("all", 0, 1.0)

def idle_gaze(sc):
    base_position = random.choice([-45, 0, 45])
    tower_1_position = random.choice([-90, 0, 90])
    bl.motor_goto('base', base_position, 0.5)
    bl.motor_goto('tower_1', tower_1_position, 0.5)

def posture_sway(sc):
    sway_position = random.randrange(3)
    bl.motor_goto('tower_1', 0, 0.5)
    if sway_position == 0:
        bl.motor_goto('tower_2', -45, 0.5)
        bl.motor_goto('tower_3', 180, 0.5)
    elif sway_position == 1:
        bl.motor_goto('tower_2', 180, 0.5)
        bl.motor_goto('tower_3', -45, 0.5)
    elif sway_position == 2:
        bl.motor_goto('tower_2', 0, 0.5)
        bl.motor_goto('tower_3', 0, 0.5)


if __name__ == "__main__":
    main()