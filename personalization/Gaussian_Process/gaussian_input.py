import sys
import board
import busio
import adafruit_mpr121
import time
import random
import pygame
import csv
sys.path.insert(1, '/home/blossom/blossom-public')

# Import light sequences
from LED.rpi_led_sequence import row_traverse, twinkle_effect, color_chase, fade_in_out, rainbow_wave, strobe_effect
from LED.motor_movements import BlossomController

bc = BlossomController()
pygame.init()
pygame.mixer.init()


# Light definitions
R = (255, 0, 0)
G = (0, 255, 0)
B = (0, 0, 255)
C = (0, 255, 255)
M = (255, 0, 255)
Y = (255, 255, 0)
color_list = [R, G, B, C, M, Y]
color_map = {
    0: R,
    1: G,
    2: B,
    3: C,
    4: M,
    5: Y,
}
light_seq_list = [row_traverse, twinkle_effect, color_chase, fade_in_out, rainbow_wave, strobe_effect]
sequence_dict = {
	row_traverse: 0,
	twinkle_effect: 1,
	color_chase: 2,
	fade_in_out: 3,
	rainbow_wave: 4,
	strobe_effect: 5
}
sound_list = [
"/home/blossom/blossom-public/final_sounds_new_categories/animal_recordings/cat_meow_16.wav",
"/home/blossom/blossom-public/final_sounds_new_categories/animal_recordings/cat_purr_16.wav",
"/home/blossom/blossom-public/final_sounds_new_categories/animal_recordings/dog_whimper.wav",
"/home/blossom/blossom-public/final_sounds_new_categories/animal_recordings/guinea_pig.wav",

"/home/blossom/blossom-public/final_sounds_new_categories/animal_vocables/S29_MEOW_1.wav",
"/home/blossom/blossom-public/final_sounds_new_categories/animal_vocables/S44_SNEEZE_2.wav",
"/home/blossom/blossom-public/final_sounds_new_categories/animal_vocables/S72_PURR_3.wav",
"/home/blossom/blossom-public/final_sounds_new_categories/animal_vocables/S89_BARK_1.wav",

"/home/blossom/blossom-public/final_sounds_new_categories/electronic_noises/Beep4.wav",
"/home/blossom/blossom-public/final_sounds_new_categories/electronic_noises/LIKED_MOMENT_2.wav",
"/home/blossom/blossom-public/final_sounds_new_categories/electronic_noises/S77_FUNCTIONAL_SUCCESS.wav",
"/home/blossom/blossom-public/final_sounds_new_categories/electronic_noises/shutter_2.wav",

"/home/blossom/blossom-public/final_sounds_new_categories/human_vocables/No.wav",
"/home/blossom/blossom-public/final_sounds_new_categories/human_vocables/S19_WHAT_THE_HECK_2.wav",
"/home/blossom/blossom-public/final_sounds_new_categories/human_vocables/Yes.wav",
"/home/blossom/blossom-public/final_sounds_new_categories/human_vocables/YOURE_WELCOME.wav"
]
motor_movements_list = [bc.sigh, bc.idle_gaze, bc.posture_sway]

# Sound and motor movement definitions
num_sounds = 16  # Number of distinct sounds
num_motor_movements = 3  # Number of distinct motor movements
motor_repeats = 4  # Each motor movement is played 4 times

# Prepare the action space
action_space = []

# Add lights - need to fix this
start_index = 0
color_index = 0
for sequence in light_seq_list:
	for i in range(3):
		color_index = start_index + i
		if color_index >= len(color_list):
			color_index -= len(color_list) 
		action_space.append((sequence_dict[sequence], color_index, -1, -1, -1))
		#action_space.append(("light", index, sequence_dict[sequence]))
	start_index += 1


# Add sounds
for sound_index in range(num_sounds):
    #action_space.append(("sound", sound_index, None))
    action_space.append((-1, -1, sound_index, sound_index // 4, -1)) #sound index // 4 represents sound category
    

# Add motor movements
for motor_index in range(num_motor_movements):
    for repeat in range(motor_repeats):
        #action_space.append(("motor", motor_index, repeat))
        action_space.append((-1, -1, -1, -1, motor_index))

# Interaction loop
random.shuffle(action_space)
data = [['light_index', 'color', 'sound_index', 'sound_category', 'movement', 'response']]  # CSV header
for action in action_space:
    light_index, color, sound_index, sound_category, movement = action
    if light_index != -1:
        #color_name = color_map[color]
        print(f"Now playing light sequence {light_index + 1} with color {color}")
        light_seq_list[light_index](color_map[color])  # Play the light sequence
        
    elif sound_index != -1:
        print(f"Now playing sound {sound_index + 1} in category {sound_category + 1}")
        pygame.mixer.music.load(sound_list[sound_index])  # Play the sound
        pygame.mixer.music.play()
        time.sleep(3)
        pygame.mixer.stop()
        
    elif movement != -1:
        print(f"Now performing motor movement {movement + 1}")
        motor_movements_list[movement]()  # Perform the motor movement

    # Get user feedback
    strInput = input("How did you feel about that behavior? Enter 1 for positive, 0 for neutral, or -1 for negative.\n")
    while strInput not in {'1', '0', '-1'}:
        strInput = input("How did you feel about that behavior? Enter 1 for positive, 0 for neutral, or -1 for negative.\n")
    
    # Record response
    data.append([light_index, color, sound_index, sound_category, movement, strInput])

# Write data to CSV
with open('gaussian_responses.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

