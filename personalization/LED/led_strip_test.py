import board
import neopixel

# Update this with the number of LEDs in the strip
num_pixels = 15

# GPIO pin connected to the DIN pin of the LED strip
pixel_pin = board.D18

# set up the LED strip
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness = 0.5, auto_write=False)

# Example: set all LEDs to red
pixels.fill((255, 0, 0))
pixels.show()