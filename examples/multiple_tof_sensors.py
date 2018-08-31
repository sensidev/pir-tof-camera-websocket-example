#!/usr/bin/python

import time

import RPi.GPIO as GPIO

from VL53L0X_rasp_python.python import VL53L0X

# GPIO for Sensor 1 shutdown pin
sensor1_shutdown_pin = 23
# GPIO for Sensor 2 shutdown pin
sensor2_shutdown_pin = 24

# Setup GPIO for shutdown pins on each VL53L0X
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor1_shutdown_pin, GPIO.OUT)
GPIO.setup(sensor2_shutdown_pin, GPIO.OUT)

# Set all shutdown pins low to turn off each VL53L0X
GPIO.output(sensor1_shutdown_pin, GPIO.LOW)
GPIO.output(sensor2_shutdown_pin, GPIO.LOW)

# Keep all low for 500 ms or so to make sure they reset
time.sleep(0.50)

# Create one object per VL53L0X passing the address to give to
# each.
sensor1 = VL53L0X.VL53L0X(address=0x2B)
sensor2 = VL53L0X.VL53L0X(address=0x2D)

# Set shutdown pin high for the first VL53L0X then
# call to start ranging
GPIO.output(sensor1_shutdown_pin, GPIO.HIGH)
time.sleep(0.50)
sensor1.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

# Set shutdown pin high for the second VL53L0X then
# call to start ranging
GPIO.output(sensor2_shutdown_pin, GPIO.HIGH)
time.sleep(0.50)
sensor2.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

timing = sensor1.get_timing()
if timing < 20000:
    timing = 20000

print("Sampling each %d ms" % (timing / 1000))

for count in range(1, 301):
    print("Sensor {sensor}: {distance} mm".format(sensor=1, distance=sensor1.get_distance()))
    print("Sensor {sensor}: {distance} mm".format(sensor=2, distance=sensor2.get_distance()))
    time.sleep(timing / 1000000.00)

sensor2.stop_ranging()
GPIO.output(sensor2_shutdown_pin, GPIO.LOW)

sensor1.stop_ranging()
GPIO.output(sensor1_shutdown_pin, GPIO.LOW)
