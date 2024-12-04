import sys
import board
import busio
import adafruit_mpr121
import time
import random
import pygame
import csv
import pandas as pd
sys.path.insert(1, '/home/blossom/blossom-public')

import numpy as np
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.gaussian_process.kernels import RationalQuadratic
from sklearn.preprocessing import OneHotEncoder

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
    0: 'red',
    1: 'green',
    2: 'blue',
    3: 'cyan',
    4: 'magenta',
    5: 'yellow',
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

motor_map = {
	0: "sigh",
	1: "idle gaze",
	2: "posture sway"
}

motor_movements_list = [bc.sigh, bc.idle_gaze, bc.posture_sway]

def perform_action(action):
    light_index, color, sound_index, sound_category, movement = action
    
    if sound_index != -1:
        print(f"Now playing sound {sound_index + 1} in category {sound_category + 1}")
        pygame.mixer.music.load(sound_list[sound_index])  # Play the sound
        pygame.mixer.music.play()
        
    if movement != -1:
        print(f"Now performing motor movement {movement + 1}")
        motor_movements_list[movement]()  # Perform the motor movement
        
    if light_index != -1:
        #color_name = color_map[color]
        print(f"Now playing light sequence {light_index + 1} with color {color}")
        light_seq_list[light_index](color_list[color])  # Play the light sequence

# Load data from the CSV file
def load_data(filename):
    # Load the data into a pandas DataFrame
    data = pd.read_csv(filename)
    
    # Define categorical columns
    categorical_cols = ['light_index', 'color', 'sound_index', 'sound_category', 'movement']
    
    # Convert all columns to categorical type
    for col in categorical_cols:
        data[col] = data[col].astype('category')
    
    # One-hot encode the categorical features
    X = pd.get_dummies(data[categorical_cols], drop_first=False).values.tolist()
    Y = data['response'].tolist()
    
    return X, Y

# Train Gaussian Process Classification model
def train_model(X, y):
    # Define the kernel: RBF with a length scale of 1.0
    kernel = 1.0 * RBF(length_scale=0.7)  # RBF kernel with default length scale
    # kernel = 1.0 * RationalQuadratic(length_scale=1.0, alpha=0.1)  # RBF kernel with default length scale

    # Initialize the Gaussian Process Classifier with the defined kernel
    model = GaussianProcessClassifier(kernel=kernel, random_state=0)
    
    # Fit the model on the provided data
    model.fit(X, y)

    # Return the trained model
    return model



# Find the most uncertain action

def pick_uncertain_behavior(model, action_space):
    uncertainties = []
    # Initialize an empty DataFrame with the correct columns
    data = pd.DataFrame(columns=['light_index', 'color', 'sound_index', 'sound_category', 'movement'])
    for action in action_space:
        # Add the new data to the DataFrame
        new_row = {
            'light_index': action[0],
            'color': action[1],
            'sound_index': action[2],
            'sound_category': action[3],
            'movement': action[4]
        }
        data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
    
    # Define categorical columns
    categorical_cols = ['light_index', 'color', 'sound_index', 'sound_category', 'movement']
           # Convert all columns to categorical type
    for col in categorical_cols:
        data[col] = data[col].astype('category')
    data = pd.get_dummies(data[categorical_cols], drop_first=False).values.tolist()
    
    for action in data:
 
    # One-hot encode the categorical features

        # One-hot encode the action and predict uncertainty (probabilities or confidence)
        action_input = np.array([action])  # Reshaping to match model input
        action_input.reshape(1, -1)
        probs = model.predict_proba(action_input)  # Get probability distribution for each class
        
        # Calculate uncertainty: This can be based on the entropy of the probability distribution
        uncertainty = -np.sum(probs * np.log(probs), axis=1)  # Entropy calculation
        uncertainties.append(uncertainty[0])
    
    most_uncertain_action = action_space[np.argmax(uncertainties)]
    return most_uncertain_action

def perform_next_action_active(action_response_filename, action_space):
    
    # Load and preprocess data
    action_response_data = pd.read_csv(action_response_filename)
    X, y = load_data(action_response_filename)

    # Train the GPC model
    model = train_model(X, y)

    # Pick the most uncertain behavior
    action = pick_uncertain_behavior(model, action_space)
    print(f"Performing most uncertain behavior: {action}")

    # Perform the action
    perform_action(action)  # Ensure this function triggers the robot action

    # Get user feedback
    strInput = input("How did you feel about that behavior? Enter 1 for positive, 0 for neutral, or -1 for negative.\n")
    while strInput not in {'1', '0', '-1'}:
        strInput = input("How did you feel about that behavior? Enter 1 for positive, 0 for neutral, or -1 for negative.\n")
    
    # Add the new data to the DataFrame
    new_row = {
        'light_index': action[0],
        'color': action[1],
        'sound_index': action[2],
        'sound_category': action[3],
        'movement': action[4],
        'response': int(strInput)
    }
    action_response_data = pd.concat([action_response_data, pd.DataFrame([new_row])], ignore_index=True)

    # Save data to CSV
    action_response_data.to_csv(action_response_filename, index=False)

def perform_next_action_random(action_response_filename, action_space):
    
    # Load and preprocess data
    action_response_data = pd.read_csv(action_response_filename)

    # Pick the most uncertain behavior
    action = random.choice(action_space)
    print(f"Performing most uncertain behavior: {action}")

    # Perform the action
    perform_action(action)  # Ensure this function triggers the robot action

    # Get user feedback
    strInput = input("How did you feel about that behavior? Enter 1 for positive, 0 for neutral, or -1 for negative.\n")
    while strInput not in {'1', '0', '-1'}:
        strInput = input("How did you feel about that behavior? Enter 1 for positive, 0 for neutral, or -1 for negative.\n")
    
    # Add the new data to the DataFrame
    new_row = {
        'light_index': action[0],
        'color': action[1],
        'sound_index': action[2],
        'sound_category': action[3],
        'movement': action[4],
        'response': int(strInput)
    }
    action_response_data = pd.concat([action_response_data, pd.DataFrame([new_row])], ignore_index=True)

    # Save data to CSV
    action_response_data.to_csv(action_response_filename, index=False)

# Step 1: Perform all single-feature actions
# Define the single-feature action space
single_feature_action_space = []

# Add lights (unimodal)
# for sequence in light_seq_list:
    # for i in range(3):  # 3 colors (R, G, B)
        # single_feature_action_space.append((sequence_dict[sequence], i, -1, -1, -1))
        
# Add lights - need to fix this
start_index = 0
color_index = 0
for sequence in light_seq_list:
	for i in range(3):
		color_index = start_index + i
		if color_index >= len(color_list):
			color_index -= len(color_list) 
		single_feature_action_space.append((sequence_dict[sequence], color_index, -1, -1, -1))
		#action_space.append(("light", index, sequence_dict[sequence]))
	start_index += 1

# Add sounds (unimodal)
for sound_index in range(len(sound_list)):
    single_feature_action_space.append((-1, -1, sound_index, sound_index // 4, -1))  # sound index // 4 represents sound category

# Add motor movements (unimodal)
for motor_index in range(len(motor_map)):
    single_feature_action_space.append((-1, -1, -1, -1, motor_index))

# Randomize order
random.shuffle(single_feature_action_space)

# Initialize an empty DataFrame with the correct columns
data = pd.DataFrame(columns=['light_index', 'color', 'sound_index', 'sound_category', 'movement', 'response'])

for action in single_feature_action_space:
    perform_action(action)
    
    # Get user feedback
    strInput = input("How did you feel about that behavior? Enter 1 for positive, 0 for neutral, or -1 for negative.\n")
    while strInput not in {'1', '0', '-1'}:
        strInput = input("How did you feel about that behavior? Enter 1 for positive, 0 for neutral, or -1 for negative.\n")
    
    # Add the new data to the DataFrame
    new_row = {
        'light_index': action[0],
        'color': action[1],
        'sound_index': action[2],
        'sound_category': action[3],
        'movement': action[4],
        'response': int(strInput)
    }
    data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)

# Save data to CSV
data.to_csv('al_responses.csv', index=False)
data.to_csv('rand_responses.csv', index=False)   

# Create the second action space (all combinations)
multi_feature_action_space = []
for sequence in light_seq_list:
    for color in range(len(color_list)):
        for sound_index in range(len(sound_list)):
            for movement in range(len(motor_map)):
                multi_feature_action_space.append((sequence_dict[sequence], color, sound_index, sound_index // 4, movement)) 
                
for sound_index in range(len(sound_list)):
    for movement in range(len(motor_map)):
        multi_feature_action_space.append((-1, -1, sound_index, sound_index // 4, movement)) 
        
for sequence in light_seq_list:
    for color in range(len(color_list)):
        for movement in range(len(motor_map)):
            multi_feature_action_space.append((sequence_dict[sequence], color, -1, -1, movement)) 
            
for sequence in light_seq_list:
    for color in range(len(color_list)):
        for sound_index in range(len(sound_list)):
            multi_feature_action_space.append((sequence_dict[sequence], color, sound_index, sound_index // 4, -1)) 

# Step 2: Alternate between Active and Random sampling for 22 rounds
for i in range(22):
    # Active: 
    perform_next_action_active('al_responses.csv', multi_feature_action_space)

    # Random
    perform_next_action_random('rand_responses.csv', multi_feature_action_space)


