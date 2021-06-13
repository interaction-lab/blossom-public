from .src import RobotConfig
from .src import SequenceRobot
from .src import CLI
import threading
from time import sleep


class Blossom():
    def __init__(self, name="woody", sequence_dir='blossompy/src/sequences'):
        self.name = name
        self.sequence_dir = sequence_dir
        self.configs = RobotConfig().get_configs([self.name])


    def connect(self):
        print("Connecting to robot")
        self.robot = SequenceRobot(self.name, self.configs[self.name], sequence_dir=self.sequence_dir)
        self.configs.pop(self.name)

        print("creating CLI")
        self.interface = CLI(self.robot)

    def load_sequences(self):
        self.robot.load_all_sequences()

    def do_sequence(self, sequence):
        if sequence in self.robot.seq_list:
            # print("Playing sequence: %s"%(args[0]))
            # iterate through all robots
            if not self.robot.seq_stop:
                self.robot.seq_stop = threading.Event()
            self.robot.seq_stop.set()
            print(sequence)
            seq_thread = self.robot.play_recording(sequence, idler=False)
        # sequence not found
        else:
            print("Unknown sequence name:", sequence)
            return

    def motor_adjust(self, motor_name, increment):
        print("Incremental adjustment not implemented yet")
        pass

    def motor_goto(self, motor_name, position, duration=0.1):
        if (motor_name == 'all'):
            self.robot.goto_position({'tower_1': float(position), 'tower_2': float(
                position), 'tower_3': float(position)}, duration, False)
        else:
            self.robot.goto_position({motor_name: float(position)}, duration, False)

    def cli(self):
        self.interface.run_cli()


