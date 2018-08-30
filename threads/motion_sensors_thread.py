import json
from threading import Thread
from time import time

from gpiozero import MotionSensor


class MotionSensorsThread(Thread):
    def __init__(self, websocket_server):
        super(MotionSensorsThread, self).__init__()

        print('Initializing motion sensors thread')

        self.websocket_server = websocket_server
        self.should_run = True

        self.pir = MotionSensor(4)
        self.pir.when_motion = self._when_motion

        self.payload_dict = {}

    def run(self):
        try:
            while self.should_run:
                pass

        finally:
            pass

    def stop(self):
        print('Finishing motion sensors thread ...')

        self.should_run = False

    def _when_motion(self):
        self.payload_dict['pir1'] = {
            'value': self.pir.motion_detected,
            'timestamp': time()
        }
        self.websocket_server.manager.broadcast(json.dumps(self.payload_dict), binary=False)
