import json
from threading import Thread
from time import time

from gpiozero import MotionSensor


class MotionSensorsThread(Thread):
    """
    Thread sampling PIR sensors and broadcast whenever one of the sensors detect motion.
    """

    def __init__(self, websocket_server, sensors=None):
        """
        Initiate PIR sensors.
        :param websocket_server: Websocket server
        :param sensors: list of objects like {'pin': 4}
        """
        super(MotionSensorsThread, self).__init__()

        print('Initializing motion sensors thread')

        self.websocket_server = websocket_server
        self.should_run = True

        self.sensors = sensors

        for s in self.sensors:
            s['instance'] = MotionSensor(s.get('pin'))
            s['instance'].when_motion = lambda instance: self._detect_motion_for(instance)

    def run(self):
        try:
            while self.should_run:
                pass

        finally:
            pass

    def stop(self):
        print('Finishing motion sensors thread ...')

        self.should_run = False

    def _detect_motion_for(self, sensor_instance):
        print('Detect Motion For PIR sensor: {}'.format(sensor_instance.pin.number))
        payload = {
            'sensor_type': 'PIR',
            'pin': sensor_instance.pin.number,
            'value': sensor_instance.motion_detected,
            'timestamp': time()
        }
        self.websocket_server.manager.broadcast(json.dumps(payload), binary=False)
