import argparse, sys
sys.path.append("..")
from blossompy import Blossom
from time import sleep
import random
import sched

from log_session import SessionLogger

# class Idle():
#     def __init__(self, bl):
#         self.do_idle = False

#     def start(self):
#         self.do_idle = True
#         sc = sched.scheduler()
#         while self.do_idle:
#             sc.enter(60, 1, sigh, (sc,))
#             sc.enter(20, 1, idle_gaze, (sc,))
#             sc.enter(25, 1, posture_sway, (sc,))
#             sc.run()
    
#     def end(self):
#         self.do_idle = False

#     def sigh(sc):
#         bl.motor_goto("all", 90, 1.0)
#         sleep(2)
#         bl.motor_goto("all", 0, 1.0)

#     def idle_gaze(sc):
#         base_position = random.choice([-45, 0, 45])
#         tower_1_position = random.choice([-90, 0, 90])
#         bl.motor_goto('base', base_position, 0.5)
#         bl.motor_goto('tower_1', tower_1_position, 0.5)

#     def posture_sway(sc):
#         sway_position = random.randrange(3)
#         bl.motor_goto('tower_1', 0, 0.5)
#         if sway_position == 0:
#             bl.motor_goto('tower_2', -45, 0.5)
#             bl.motor_goto('tower_3', 180, 0.5)
#         elif sway_position == 1:
#             bl.motor_goto('tower_2', 180, 0.5)
#             bl.motor_goto('tower_3', -45, 0.5)
#         elif sway_position == 2:
#             bl.motor_goto('tower_2', 0, 0.5)
#             bl.motor_goto('tower_3', 0, 0.5)

class BlossomController():
    def __init__(self):
        self.do_idle = False
        self.bl = Blossom(name="woody")
        self.bl.connect()

        self.logger = SessionLogger("blossom_behavior_log")

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

############################################
# bl = Blossom()

# def main():
#     """
#     Start robots, start up server, handle CLI
#     ToDo: the multi-robot setup should be a seperate file
#     """
#     bl.connect() # safe init and connects to blossom and puts blossom in reset position

#     sc = sched.scheduler()
#     while 1:
#         sc.enter(60, 1, sigh, (sc,))
#         sc.enter(20, 1, idle_gaze, (sc,))
#         sc.enter(25, 1, posture_sway, (sc,))
#         sc.run()
    

# def sigh(sc):
#     print("performing sigh")
#     bl.motor_goto("all", 90, 1.0)
#     sleep(2)
#     bl.motor_goto("all", 0, 1.0)

# def idle_gaze(sc):
#     base_position = random.choice([-45, 0, 45])
#     tower_1_position = random.choice([-90, 0, 90])
#     print("performing idle gaze")
#     bl.motor_goto('base', base_position, 0.5)
#     bl.motor_goto('tower_1', tower_1_position, 0.5)

# def posture_sway(sc):
#     sway_position = random.randrange(3)
#     print("performing posture sway")
#     bl.motor_goto('tower_1', 0, 0.5)
#     if sway_position == 0:
#         bl.motor_goto('tower_2', -45, 0.5)
#         bl.motor_goto('tower_3', 180, 0.5)
#     elif sway_position == 1:
#         bl.motor_goto('tower_2', 180, 0.5)
#         bl.motor_goto('tower_3', -45, 0.5)
#     elif sway_position == 2:
#         bl.motor_goto('tower_2', 0, 0.5)
#         bl.motor_goto('tower_3', 0, 0.5)


# if __name__ == "__main__":
#     main()