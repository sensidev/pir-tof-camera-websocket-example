import json
from threading import Thread
from time import time

from gpiozero import MotionSensor


class MotionSensorsThread(Thread):
    """
    Thread sampling PIR sensors and broadcast whenever one of the sensors detect motion.
    """

    WHEN_MOTION_VALUE = 1000

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
        self._init_sensors_state_dict()

        for s in self.sensors:
            s['instance'] = MotionSensor(s.get('pin'))
            s['instance'].when_motion = lambda instance: self._detect_event_for(instance)

    def run(self):
        try:
            while self.should_run:
                pass

        finally:
            pass

    def stop(self):
        print('Finishing motion sensors thread ...')

        self.should_run = False

    def _get_payload(self):
        payload = {
            "type": "motion",
            "samples": []
        }
        for i, s in enumerate(self.sensors, start=1):
            pin = s.get('pin')

            payload['samples'].append({
                'id': 'motion-sensor-{}'.format(i),
                'pin': pin,
                'sample': self.sensor_state_dict[pin],
            })

        return payload

    def _detect_event_for(self, sensor_instance):
        print('Detect Event For PIR sensor: {}'.format(sensor_instance.pin.number))
        print('Motion detected: {}'.format(sensor_instance.motion_detected))

        self.sensor_state_dict[sensor_instance.pin.number] = {
            'value': self.WHEN_MOTION_VALUE if sensor_instance.motion_detected else 0,
            'timestamp': time()
        }

        self.websocket_server.manager.broadcast(json.dumps(self._get_payload()), binary=False)

    def _init_sensors_state_dict(self):
        self.sensor_state_dict = {
            s.get('pin'): {'value': 0, 'timestamp': time()} for s in self.sensors
        }
