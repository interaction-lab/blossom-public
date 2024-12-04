import board
import busio
import adafruit_mpr121
import time

# Create I2C bus object
i2c = busio.I2C(board.SCL, board.SDA)

# Create MPR121 object
mpr121 = adafruit_mpr121.MPR121(i2c)

print("MPR121 Capacitive Touch Sensor Test")
time.sleep(0.5)
while True:
    if mpr121.filtered_data(8) < 150:
        print(f"Input touched!")
    time.sleep(0.1)
