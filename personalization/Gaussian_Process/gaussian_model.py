import csv
import numpy as np
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.preprocessing import OneHotEncoder

sequence_dict = {
	0: "row_traverse",
	1: "twinkle_effect",
	2: "color_chase",
	3: "fade_in_out",
	4: "rainbow_wave",
	5: "strobe_effect"
}
color_map = {
    0: 'red',
    1: 'green',
    2: 'blue',
    3: 'cyan',
    4: 'magenta',
    5: 'yellow',
}
sound_map = {
	0:"/home/blossom/blossom-public/final_sounds_new_categories/animal_recordings/cat_meow.wav",
	1:"/home/blossom/blossom-public/final_sounds_new_categories/animal_recordings/cat_purr.wav",
	2:"/home/blossom/blossom-public/final_sounds_new_categories/animal_recordings/dog_whimper.wav",
	3:"/home/blossom/blossom-public/final_sounds_new_categories/animal_recordings/guinea_pig.wav",

	4:"/home/blossom/blossom-public/final_sounds_new_categories/animal_vocables/S29_MEOW_1.wav",
	5:"/home/blossom/blossom-public/final_sounds_new_categories/animal_vocables/S44_SNEEZE_2.wav",
	6:"/home/blossom/blossom-public/final_sounds_new_categories/animal_vocables/S72_PURR_3.wav",
	7:"/home/blossom/blossom-public/final_sounds_new_categories/animal_vocables/S89_BARK_1.wav",

	8:"/home/blossom/blossom-public/final_sounds_new_categories/electronic_noises/Beep4.wav",
	9:"/home/blossom/blossom-public/final_sounds_new_categories/electronic_noises/LIKED_MOMENT_2.wav",
	10:"/home/blossom/blossom-public/final_sounds_new_categories/electronic_noises/S77_FUNCTIONAL_SUCCESS.wav",
	11:"/home/blossom/blossom-public/final_sounds_new_categories/electronic_noises/shutter_2.wav",

	12:"/home/blossom/blossom-public/final_sounds_new_categories/human_vocables/No.wav",
	13:"/home/blossom/blossom-public/final_sounds_new_categories/human_vocables/S19_WHAT_THE_HECK_2.wav",
	14:"/home/blossom/blossom-public/final_sounds_new_categories/human_vocables/Yes.wav",
	15:"/home/blossom/blossom-public/final_sounds_new_categories/human_vocables/YOURE_WELCOME.wav"
}
motor_map = {
	0: "sigh",
	1: "idle gaze",
	2: "posture sway"
}

# Load data from the CSV file
def load_data(filename):
    X = []
    Y = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Parse type, identifier, sequence, and response
            light_index = int(row['light_index'])
            color = int(row['color'])
            sound_index = int(row['sound_index'])
            sound_category = int(row['sound_category'])
            movement = int(row['movement'])
            response = int(row['response'])
            X.append([light_index, color, sound_index, sound_category, movement])
            Y.append(int(row['response']))
    return X, Y

# Train Gaussian Process Classification model
def train_model(X, y):
    kernel = 1.0 * RBF(length_scale=1.0)  # Use RBF kernel
    model = GaussianProcessClassifier(kernel=kernel, random_state=0)
    model.fit(X, y)
    return model

# Pick the next most uncertain behavior
def pick_uncertain_behavior(model, action_space):
    variances = []
    for behavior in action_space:
        # Reshape behavior for prediction
        behavior_features = np.array(behavior).reshape(1, -1)
        probabilities = model.predict_proba(behavior_features)[0]
        max_probability = np.max(probabilities)
        variance = max_probability * (1 - max_probability)
        variances.append(variance)
    # Find the behavior with the highest uncertainty
    most_uncertain_index = np.argmax(variances)
    return action_space[most_uncertain_index]

# Main script
if __name__ == "__main__":
    # Load and preprocess data
    X, y = load_data('gaussian_responses.csv')
    #X, y = preprocess_data(data)

    # Train the GPC model
    model = train_model(X, y)

    # Define the action space (example action space for lights, sounds, and motor movements)
    action_space = []
    for light_index in range(6):
        for color in range(6):
            for sound_index in range(16):
                for movement in range(3):
                    action_space.append([light_index, color, sound_index, sound_index//4, movement])
    print(pick_uncertain_behavior(model, action_space))
"""
    # Add light behaviors (6 colors * 6 sequences)
    for color in range(6):
        for sequence in range(6):
            action_space.append([sequence, color, -1, -1, -1])

    # Add sound behaviors (16 sounds)
    for sound in range(16):
        action_space.append([-1, -1, sound, sound//4, -1]) #sound//4 represents the sound category 

    # Add motor behaviors (3 motor movements * 4 repeats)
    for motor in range(3):
        for repeat in range(4):
            action_space.append([-1, -1, -1, -1, motor])
"""
    # Pick the most uncertain behavior
    #light_index, color, sound_index, sound_category, movement = pick_uncertain_behavior(model, action_space)
    
"""
    if light_index != -1:
        print("Next most uncertain behavior is light sequence", sequence_dict[light_index], "with color", color_map[color])
    elif sound_index != -1:
        print("Next most uncertain behavior is sound", sound_map[sound_index], "in category", sound_index//4)
    elif movement != -1:
        print("Next most uncertain behavior is motor movement", motor_map[movement])
        """
"""
import numpy as np
import pandas as pd
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

# Load data from CSV file
def load_data(filename):
    data = pd.read_csv(filename, header=0, names=["type", "identifier", "sequence", "response"])
    color_encoder = LabelEncoder()
    print("Before encoding: ", data["color"])
    data["color"] = color_encoder.fit_transform(data["color"].astype(str)) #Force sequence to be numeric
    data.dropna(inplace=True) #Drop rows with non-numeric sequence values
    print("After encoding: ", data["color"])
    return data, color_encoder

# Define and train the model
def train_model(data):
    X = data[["color", "sequence"]].values  # Inputs: color and sequence
    y = data["response"].values  # Output: user response (1, 0, -1)
    kernel = 1.0 * RBF([1.0, 1.0])
    gpc = GaussianProcessClassifier(kernel=kernel).fit(X, y)
    return gpc

# Pick the next behavior based on model predictions
def pick_next_behavior(model, color_encoder):
    # Generate all possible behaviors (36 combinations of color and sequence)
    behaviors = np.array([(color, seq) for color in range(6) for seq in range(6)])
    
    # Predict probabilities for each behavior
    probabilities = model.predict_proba(behaviors)
    
    # Choose behavior with highest positive response probability
    positive_probs = probabilities[:, 2]  # Assuming index 2 corresponds to response=1
    best_behavior_index = np.argmax(positive_probs)
    best_behavior = behaviors[best_behavior_index]
    
    # Decode color
    color_name = color_encoder.inverse_transform([best_behavior[0]])[0]
    sequence = best_behavior[1]
    
    return color_name, sequence

# Pick the next behavior based on model uncertainty across all 36 behaviors 
def pick_uncertain_behavior(model, color_encoder):
	# Generate and encode behaviors 
	all_behaviors = [(color, seq) for color in range(6) for seq in range(6)] 
	behaviors = np.array([(color, seq) for color, seq in all_behaviors]) 
	
	# Predict probabilities 
	variances = []
	for action in behaviors:
		proba = model.predict_proba(action.reshape(1, -1))[0]
		max_proba = np.max(proba)
		variances.append(max_proba * (1 - max_proba))
	
	#Plot action space
	x = behaviors[:, 0]
	y = behaviors[:, 1]
	plt.scatter(x, y, c=variances, cmap='viridis', s=50)
	plt.colorbar(label="Predictive Variance")
	plt.xlabel("Color")
	plt.ylabel("Sequence")
	plt.show()
	
	#Find index and corresponding value of most uncertain value
	uncertain_behavior_index = np.argmax(variances) 
	uncertain_behavior = behaviors[uncertain_behavior_index]
	
	#Convert encoded behavior back to original color and sequence
	color_name = color_encoder.inverse_transform([uncertain_behavior[0]])[0] 
	sequence = uncertain_behavior[1] 
	return color_name, sequence


	

# Main script
filename = "gaussian_responses.csv" 
data, color_encoder = load_data(filename)
model = train_model(data)
#next_color, next_sequence = pick_next_behavior(model, color_encoder)

#print("Next behavior to play:")
#print(f"Color: {next_color}, Sequence: {next_sequence}")

uncertain_color, uncertain_sequence = pick_uncertain_behavior(model, color_encoder) 
print("Next behavior based on uncertainty:") 
print(f"Color: {uncertain_color}, Sequence: {uncertain_sequence}")
"""
