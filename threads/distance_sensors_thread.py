import collections
import json
from threading import Thread
from time import sleep, time

from VL53L0X_rasp_python.python import VL53L0X


class DistanceSensorsThread(Thread):
    NUMBER_OF_SAMPLES = 16

    def __init__(self, websocket_server):
        super(DistanceSensorsThread, self).__init__()

        print('Initializing distance sensors thread')

        self.websocket_server = websocket_server
        self.should_run = True

        self.tof_sensor = VL53L0X.VL53L0X()
        self.tof_sensor.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

        self.sampling_rate_ms = self.tof_sensor.get_timing() / 1000.0

        self.payloads_dict = collections.defaultdict(lambda: [])

    def run(self):
        try:
            while self.should_run:
                for i in range(self.NUMBER_OF_SAMPLES):
                    self.payloads_dict['tof1'].append({
                        'value': self.tof_sensor.get_distance(),
                        'timestamp': time()
                    })
                    sleep(self.sampling_rate_ms / 1000.0)

                self.websocket_server.manager.broadcast(self.get_payloads_dict_dump(), binary=False)
                self.clean_payloads_dict()
        finally:
            pass

    def stop(self):
        print('Finishing distance sensors thread ...')

        self.should_run = False
        self.tof_sensor.stop_ranging()

    def get_payloads_dict_dump(self):
        return json.dumps(self.payloads_dict)

    def clean_payloads_dict(self):
        self.payloads_dict = collections.defaultdict(lambda: [])
