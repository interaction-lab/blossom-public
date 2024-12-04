import time
import board
import neopixel
import random

# Number of LEDs in the strip
num_pixels = 38

# GPIO pin connected to the DIN of the LED strip
pixel_pin = board.D21

# Set up the LED strip
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.6, auto_write=False)

# Define some colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)
OFF = (0, 0, 0)
WHITE = (255, 255, 255)

RAINBOW_COLORS = [
    (255, 0, 0), #Red
    (255, 127, 0), #Orange
    (255, 255, 0), #Yellow
    (0, 255, 0), #Green
    (0, 0, 255), #Blue
    (75, 0, 130), #Indigo
]

colors = [
    (255, 0, 0),      # Red
    (255, 128, 0),    # Orange
    (255, 255, 0),    # Yellow
    (128, 255, 0),    # Yellow-Green
    (0, 255, 0),      # Green
    (0, 255, 128),    # Spring Green
    (0, 255, 255),    # Cyan
    (0, 128, 255),    # Light Blue
    (0, 0, 255),      # Blue
    (128, 0, 255),    # Blue-Violet
    (255, 0, 255),    # Magenta
    (255, 0, 128),    # Rose
    (255, 192, 203),  # Pink
    (255, 105, 180),  # Hot Pink
    (255, 69, 0),     # Red-Orange
    (255, 20, 147),   # Deep Pink
    (75, 0, 130),     # Indigo
    (238, 130, 238),  # Violet
    (148, 0, 211),    # Dark Violet
    (139, 0, 139),    # Dark Magenta
    (128, 128, 128),  # Gray
    (192, 192, 192),  # Silver
    (255, 255, 255),  # White
    (0, 0, 0),        # Black
    (165, 42, 42),    # Brown
    (255, 228, 196),  # Bisque
    (255, 140, 0),    # Dark Orange
    (255, 215, 0),    # Gold
    (0, 100, 0),      # Dark Green
    (0, 191, 255),    # Deep Sky Blue
    (70, 130, 180),   # Steel Blue
    (65, 105, 225),    # Royal Blue
    (238, 221, 130),  # Pale Goldenrod
    (255, 250, 205),  # Lemon Chiffon
    (255, 160, 122),  # Light Salmon
    (255, 182, 193),  # Light Pink
    (221, 160, 221),  # Plum
    (240, 230, 140),  # Khaki
    (240, 128, 128),  # Light Coral
    (255, 105, 180),  # Hot Pink
    (186, 85, 211),   # Medium Orchid
    (75, 0, 130),     # Indigo
]
    

# Function to create a color wheel effect
def color_wheel(pos):
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

# Function to create a rainbow cycle across the LEDs
def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = color_wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

# Light sequence 1
def color_chase(color, wait=0.04):
    for i in range(num_pixels):
        pixels[i] = color
        pixels.show()
        time.sleep(wait)
        pixels[i] = OFF  # Turn off the previous LED

# Light sequence 8
def fade_in_out(color, steps=200):
    for brightness in range(steps):
        pixels.fill((color[0] * brightness // steps, color[1] * brightness // steps, color[2] * brightness // steps))
        pixels.show()
        time.sleep(0.002)
    for brightness in range(steps, -1, -1):
        pixels.fill((color[0] * brightness // steps, color[1] * brightness // steps, color[2] * brightness // steps))
        pixels.show()
        time.sleep(0.002)

def all_on_off(color):
    for i in range(num_pixels):
        pixels[i] = color
    pixels.show()
    time.sleep(2)  # Hold the color for 2 seconds

    for i in range(num_pixels):
        pixels[i] = (0, 0, 0)  # Turn off
    pixels.show()

def rainbow_wave(color):
    for i in range(num_pixels):
        pixels[i] = color  # Set each pixel to the color
        pixels.show()
        time.sleep(0.05)  # Slight delay for a wave effect
    
    for i in range(num_pixels):
        pixels[i] = (0, 0, 0)  # Turn off
    pixels.show()

def pulse_effect(color):
    for i in range(num_pixels): # Turn pixels on
        pixels[i] = color
        pixels.show()
    
    for brightness in range(255, -1, -5):  # Decrease brightness
        for i in range(num_pixels):
            pixels[i] = (color[0] * brightness // 255,
                         color[1] * brightness // 255,
                         color[2] * brightness // 255)
        pixels.show()
        time.sleep(0.02)
    
    for brightness in range(0, 256, 5):  # Increase brightness
        for i in range(num_pixels):
            pixels[i] = (color[0] * brightness // 255,
                         color[1] * brightness // 255,
                         color[2] * brightness // 255)
        pixels.show()
        time.sleep(0.02)

    for i in range(num_pixels): # Turn pixels off
        pixels[i] = OFF
        pixels.show()

def strobe_effect(color):
    for _ in range(10):  # Strobe effect duration
        for i in range(num_pixels):
            pixels[i] = color  # Turn on all
        pixels.show()
        time.sleep(0.1)  # Show for a brief moment
        
        for i in range(num_pixels):
            pixels[i] = (0, 0, 0)  # Turn off all
        pixels.show()
        time.sleep(0.1)  # Off for a brief moment


def twinkle_effect(color):
    initial_brightness = 0.1  # Start at 10% brightness
    max_brightness = min(1, initial_brightness + 1 * (1 - initial_brightness))  # Calculate max brightness
    
    start_time = time.time()
    while time.time() - start_time < 2:  # Duration of the effect is 2 seconds
        for i in range(num_pixels):
            # Randomly choose a twinkle brightness between the initial and max brightness
            twinkle_brightness = initial_brightness + random.uniform(0, max_brightness - initial_brightness)
            # Set the pixel color with the calculated brightness
            pixels[i] = (int(color[0] * twinkle_brightness),
                         int(color[1] * twinkle_brightness),
                         int(color[2] * twinkle_brightness))
        pixels.show()
        time.sleep(0.2)  # Short delay to create the twinkling effect

    # Turn off all pixels at the end
    for i in range(num_pixels):
        pixels[i] = (0, 0, 0)  # Set all to off
    pixels.show()



""""Trick Sequence"""
def flicker_off():
   # Step 1: Set all pixels to rainbow colors
   pixels_to_color = list(range(num_pixels))
   random.shuffle(pixels_to_color)
   for i in range(num_pixels):
       pixels[i] = colors[pixels_to_color[i]]
   pixels.show()
  
   # Step 2: Wait for 0.5 seconds
   time.sleep(0.5)


   # Step 3: Gradually turn off the LEDs
   pixels_to_turn_off = list(range(num_pixels))  # List of indices of pixels
   random.shuffle(pixels_to_turn_off)  # Shuffle to create a seemingly random order


   for i in range(num_pixels):
       # Turn off one LED at a time
       pixel_index = pixels_to_turn_off[i]
       pixels[pixel_index] = (0, 0, 0)  # Set the pixel to off
       pixels.show()
       time.sleep(1 / num_pixels)  # Spread out the turning off over 1 second


   # Step 4: Ensure all LEDs are off at the end
   for i in range(num_pixels):
       pixels[i] = (0, 0, 0)  # Explicitly set to off
   pixels.show()

""""Trick Sequence"""
def rainbow_blink(duration = 3):
    for i in range(len(RAINBOW_COLORS)):
        fade_in_out(RAINBOW_COLORS[i], steps = 100)
        #time.sleep(wait)
        #pixels[i] = OFF  # Turn off the previous LED

def row_traverse(color):
    r = color[0]
    g = color[1]
    b = color[2]
    for i in range(15):
        pixels[i] = (r, g, b)
        pixels.show()
    time.sleep(0.5)
    for i in range(15, 29):
        pixels[i] = (r, g, b)
        pixels.show()
    time.sleep(0.5)
    for i in range(29, 38):
        pixels[i] = (r, g, b)
        pixels.show()
    time.sleep(0.5)
    for i in range(29, 38):
        pixels[i] = OFF
        pixels.show()
    time.sleep(0.5)
    for i in range(15, 29):
        pixels[i] = OFF
        pixels.show()
    time.sleep(0.5)
    for i in range(15):
        pixels[i] = OFF
        pixels.show()
    time.sleep(0.5)

# Main loop to run the sequence
if __name__ == "__main__":
    while True:
        """Test trick sequences"""
    #rainbow_blink()
    #flicker_off()
    #rainbow_cycle(0.001)
    
        """Test 8 light sequences"""
    
        #pulse_effect(GREEN)
        #time.sleep(2)
        color_chase(WHITE)
        time.sleep(2)
        rainbow_wave(WHITE)
        time.sleep(2)
        row_traverse(WHITE)
        time.sleep(2)
    
        twinkle_effect(WHITE)
        time.sleep(2)
    
    
        
        fade_in_out(WHITE)
        time.sleep(2)
        #all_on_off(BLUE)
        #time.sleep(2)
        
    
        strobe_effect(WHITE)
        time.sleep(2)


