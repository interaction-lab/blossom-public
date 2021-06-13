from __future__ import print_function

import os
from .robot import Robot
from .sequence import Sequence, SequencePrimitive, RecorderPrimitive
import threading
from serial.serialutil import SerialException
from pypot.dynamixel.controller import DxlError
# import sys
# import subprocess
# import argparse
# import shutil
# import signal
# from src.config import RobotConfig
# import yaml

loaded_seq = []

class SequenceRobot(Robot):
    """
    Robot that loads, plays, and records sequences
    Extends Robot class
    """

    def __init__(self, name, config, sequence_dir='blossompy/src/sequences'):
        # init robot
        self.sequence_dir = sequence_dir
        self.safe_init_robot(name, config, attempts=10)

    def safe_init_robot(self, name, config, attempts=10):
        """
        Safely start/init robots, due to sometimes failing to start motors
        args:
            name    name of the robot to start
            config  the motor configuration of the robot
        returns:
            the started SequenceRobot object
        """
        print("Starting Safe Initialization")
        while attempts >0:
            try:
                br=57600
                super(SequenceRobot, self).__init__(config, br, name)
                # save configuration (list of motors for PyPot)
                self.config = config
                # threads for playing and recording sequences
                self.seq_thread = self.seq_stop = None
                self.rec_thread = self.rec_stop = None
                # load all sequences for this robot
                self.load_all_sequences()

                # speed, amp range from 0.5 to 1.5
                self.speed = 1.0
                self.amp = 1.0
                # posture ranges from -100 to 100
                self.post = 0.0
                attempts = 0
            except (DxlError, NotImplementedError, RuntimeError, SerialException) as e:
                if attempts <= 0:
                    raise e
                print(e, "retrying...")
                attempts -= 1
        print("Init Complete")

    def load_all_sequences(self):
        """
        Load all sequences in robot's directory
        TODO - clean this up - try glob or os.walk
        """
        # get directory
        seq_dir = os.path.join(self.sequence_dir,self.name)
        # make sure that directory for robot's seqs exist
        if not os.path.exists(seq_dir):
            os.makedirs(seq_dir)

        # iterate through sequences
        seq_names = os.listdir(seq_dir)
        seq_names.sort()
        # bar = Bar('Importing sequences',max=len(seq_names),fill='=')
        for seq in seq_names:
            # bar.next()
            subseq_dir = seq_dir + '/' + seq

            # is sequence, load
            if (seq[-5:] == '.json' and subseq_dir not in loaded_seq):
                # print("Loading {}".format(seq))
                self.load_sequences(subseq_dir)
                # loaded_seq.append(subseq_dir)

            # is subdirectory, go in and load all sequences
            # skips subdirectory if name is 'ignore'
            elif os.path.isdir(subseq_dir) and not ('ignore' in subseq_dir):
                # go through all sequence
                for s in os.listdir(subseq_dir):
                    # is sequence, load
                    seq_name = "%s/%s"%(subseq_dir,s)
                    if (s[-5:] == '.json' and seq_name not in loaded_seq):
                        # print("Loading {}".format(s))
                        self.load_sequences(seq_name)
                        # loaded_seq.append(seq_name)
        # bar.finish()
        print("Loaded sequences - ", len(self.seq_list))

    def assign_time_length(self, keys, vals):
        timeMap = [None] * len(keys)
        for i in range(0, len(keys)):
            frameLst = vals[i].frames
            if len(frameLst)!= 0:
                timeAmnt = frameLst[-1].millis
                timeMap[i] = [keys[i], str(timeAmnt / 1000)]
        return timeMap

    def get_time_sequences(self):
        tempKeys = list(self.seq_list.keys())
        tempVals = list(self.seq_list.values())
        tempMap = self.assign_time_length(tempKeys, tempVals)
        return tempMap

    def get_sequence_names(self):
        """
        Get all sequences loaded on robot
        """
        return self.seq_list.keys()

    def play_seq_json(self, seq_json):
        """
        Play a sequence from json
        args:
            seq_json    sequence raw json
        returns:
            the thread setting motor position in the sequence
        """
        seq = Sequence.from_json_object(seq_json, rad=True)
        # create stop flag object
        self.seq_stop = threading.Event()

        # start playback thread
        self.seq_thread = SequencePrimitive(
            self, seq, self.seq_stop, speed=self.speed, amp=self.amp, post=self.post)
        self.seq_thread.start()

        # return thread
        return self.seq_thread

    def play_recording(self, seq, idler=False):
        """
        Play a recorded sequence
        args:
            seq     sequence name
            idler   whether to loop sequence or not
        returns:
            the thread setting motor position in the sequence
        """
        # create stop flag object
        self.seq_stop = threading.Event()

        # loop if idler
        if ('idle' in seq):
            seq = seq.replace('idle', '').replace(' ', '').replace('/', '')
            idler = True

        # start playback thread
        self.seq_thread = SequencePrimitive(
            self, self.seq_list[seq], self.seq_stop, idler=idler, speed=self.speed, amp=self.amp, post=self.post)
        self.seq_thread.start()
        # return thread
        return self.seq_thread

    def start_recording(self):
        """
        Begin recording a sequence
        """
        # create stop flag object
        self.rec_stop = threading.Event()

        # start recording thread
        self.rec_thread = RecorderPrimitive(self, self.rec_stop)
        self.rec_thread.start()
