from blossompy import Blossom
from time import sleep

# Create Blossom object
bl = Blossom(sequence_dir='../blossompy/src/sequences', name="woody")
bl.connect()  # safe init and connects to blossom and puts blossom in reset position
bl.load_sequences() # load Blossom sequences stored in sequence_dir/woody

# Option 1: Perform pre-programmed sequences
print("performing sequence: reset")
bl.do_sequence("reset")

sleep(2)

print("performing sequence: no")
bl.do_sequence("no")

sleep(2)

print("performing sequence: yes")
bl.do_sequence("yes")

sleep(2)

# Option 2: Issue direct motor commands
bl.motor_goto("tower_1", # Motor name (tower_1, tower_2, tower_3, or base)
              90, # Position
              1.0) # Duration (default = 0.1s)

sleep(2) 

# Use "all" to move all tower motors to the same position
bl.motor_goto("all", 0, 1.0) 

# For all Blossom commands, see blossom-public/blossompy/src/main



