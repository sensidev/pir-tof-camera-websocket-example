import json
import random
from threading import Thread
from time import sleep

from gpiozero import MotionSensor

from VL53L0X_rasp_python.python import VL53L0X


class SensorsThread(Thread):
    def __init__(self, websocket_server):
        super(SensorsThread, self).__init__()

        print('Initializing sensors thread')

        self.websocket_server = websocket_server
        self.should_run = True

        self.tof_sensor = VL53L0X.VL53L0X()
        self.tof_sensor.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

        self.pir = MotionSensor(4)

    def run(self):
        try:
            while self.should_run:
                data = json.dumps({
                    'tof1': self.tof_sensor.get_distance(),
                    'pir1': random.randint(0, 2000),
                })
                self.websocket_server.manager.broadcast(data, binary=False)
                sleep(1)
        finally:
            pass

    def stop(self):
        print('Finishing sensor thread ...')

        self.should_run = False
        self.tof_sensor.stop_ranging()

    def join(self, timeout=None):
        super(SensorsThread, self).join(timeout)
