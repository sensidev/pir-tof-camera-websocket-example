from time import sleep, time

from gpiozero import MotionSensor

sensor1 = MotionSensor(4)
sensor2 = MotionSensor(14)

sensor1.when_motion = lambda _: print("Sensor1: Motion detected at {}".format(time()))
sensor2.when_motion = lambda _: print("Sensor2: Motion detected at {}".format(time()))

while True:
    sleep(3)
