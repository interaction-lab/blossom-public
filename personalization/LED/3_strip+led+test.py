import time
import board
import neopixel
import random

# Number of LEDs in each strip
num_pixels = 15

# GPIO pins connected to the DIN of the LED strips
pixel_pins = [board.D18, board.D23, board.D24]  # Example pins for three strips

# Set up the LED strips
pixels = [neopixel.NeoPixel(pin, num_pixels, brightness=0.6, auto_write=False) for pin in pixel_pins]

# Define some colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)
OFF = (0, 0, 0)

# Function to perform spiral effect
def spiral_effect(wait):
    for i in range(num_pixels):
        for strip in pixels:
            strip[i] = RED
            strip.show()
        time.sleep(wait)
        for strip in pixels:
            strip[i] = OFF
            strip.show()

# Function to blink all strips on/off together
def blink_all(wait):
    for _ in range(5):  # Blink 5 times
        for strip in pixels:
            strip.fill(RED)
            strip.show()
        time.sleep(wait)
        for strip in pixels:
            strip.fill(OFF)
            strip.show()
        time.sleep(wait)

# Function to blink one strip at a time
def blink_one(wait):
    for strip in pixels:
        strip.fill(RED)
        strip.show()
        time.sleep(wait)
        strip.fill(OFF)
        strip.show()
        time.sleep(wait)

# Function for left/right or up/down simultaneous opposite direction
def opposite_direction(wait):
    for i in range(num_pixels):
        for strip in pixels:
            strip[i] = GREEN if strip is pixels[0] else OFF
            strip[num_pixels - 1 - i] = GREEN if strip is pixels[1] else OFF
            strip.show()
        time.sleep(wait)
        for strip in pixels:
            strip.fill(OFF)
            strip.show()

# Function for left/right or up/down simultaneous same direction
def same_direction(wait):
    for i in range(num_pixels):
        for strip in pixels:
            strip[i] = BLUE
            strip.show()
        time.sleep(wait)
        for strip in pixels:
            strip.fill(OFF)
            strip.show()

# Function for lights starting in the middle and moving outward
def middle_outward(wait):
    for i in range(num_pixels // 2 + 1):
        for strip in pixels:
            strip[num_pixels // 2 + i] = CYAN
            strip[num_pixels // 2 - i] = CYAN
            strip.show()
        time.sleep(wait)
        for strip in pixels:
            strip.fill(OFF)
            strip.show()

# Function for lights starting from the outside and moving inward
def outside_inward(wait):
    for i in range(num_pixels // 2 + 1):
        for strip in pixels:
            strip[i] = PURPLE
            strip[num_pixels - 1 - i] = PURPLE
            strip.show()
        time.sleep(wait)
        for strip in pixels:
            strip.fill(OFF)
            strip.show()

# Function for random light patterns
def random_pattern(wait):
    for _ in range(5):  # Random pattern for 5 iterations
        for strip in pixels:
            for i in range(num_pixels):
                strip[i] = random.choice([RED, GREEN, BLUE, OFF])
            strip.show()
        time.sleep(wait)

# Main loop to run the sequences
while True:
    spiral_effect(0.1)
    blink_all(0.5)
    blink_one(0.5)
    opposite_direction(0.1)
    same_direction(0.1)
    middle_outward(0.1)
    outside_inward(0.1)
    random_pattern(0.2)
