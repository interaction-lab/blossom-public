import sys
import board
import busio
import adafruit_mpr121
import time
import random
import pygame

sys.path.insert(1, '/home/blossom/blossom-public')
from LED.rpi_led_sequence import pulse_effect, row_traverse, twinkle_effect, color_chase, fade_in_out, all_on_off, rainbow_wave, strobe_effect
from LED.motor_movements import BlossomController

bc = BlossomController()

# Define some colors
color_list = [(255, 0, 0),(0, 255, 0),(0, 0, 255),(255, 255, 0),(0, 255, 255),(128, 0, 128)]
light_seq_list = [pulse_effect, row_traverse, twinkle_effect, color_chase, fade_in_out, all_on_off, rainbow_wave, strobe_effect]

# Create I2C bus object
i2c = busio.I2C(board.SCL, board.SDA)

# Create MPR121 object
mpr121 = adafruit_mpr121.MPR121(i2c)

print("Touch/Behavior Test")
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('/home/blossom/Downloads/S72_PURR_1.wav')

time.sleep(0.5) #Used to prevent touch sensor from falsely detecting reading at startup
num = 0
colorNum = 0
while True:
    if mpr121.filtered_data(8) < 150:
        print("Input touched!")
        num = random.randint(0, len(light_seq_list)-1)
        colorNum = random.randint(0, len(color_list)-1)
        pygame.mixer.music.play()
        light_seq_list[num](color_list[colorNum])
        bc.sigh()
        
        time.sleep(3) #Stop sensor from taking more readings while behavior isn't finished
    time.sleep(0.1)

