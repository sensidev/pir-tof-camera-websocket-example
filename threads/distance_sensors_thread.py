import json
from threading import Thread
from time import sleep

import RPi.GPIO as GPIO

from VL53L0X_rasp_python.python import VL53L0X


class DistanceSensorsThread(Thread):
    """
    Thread sampling ToF sensors then broadcast a number of sampled values to all websocket clients.
    """
    NUMBER_OF_SAMPLES_PER_BROADCAST = 16

    def __init__(self, websocket_server, sensors=None):
        """
        Initiate ToF sensors.
        :param websocket_server: Websocket server
        :param sensors: list of objects like {'i2c_address': 0x2B, 'shutdown_pin': 23}
        """
        super(DistanceSensorsThread, self).__init__()

        print('Initializing distance sensors thread')

        self.websocket_server = websocket_server
        self.should_run = True

        if not sensors:
            raise Exception('No sensors to configure!')

        self.sensors = sensors

        self._configure_sensors()

        self.sampling_rate_ms = self._get_sampling_rate_ms()

    def run(self):
        try:
            while self.should_run:
                for _ in range(self.NUMBER_OF_SAMPLES_PER_BROADCAST):
                    self._sample_sensors()

                self.websocket_server.manager.broadcast(self._get_payload_dump(), binary=False)
                self._clean_samples()
        finally:
            pass

    def _sample_sensors(self):
        for s in self.sensors:
            s['samples'].append(s.get('instance').get_distance())
        sleep(self.sampling_rate_ms / 1000.0)

    def stop(self):
        print('Finishing distance sensors thread ...')

        self.should_run = False
        self._stop_ranging()

    def _get_payload_dump(self):
        payload = []
        for s in self.sensors:
            payload.append(s.get('samples'))

        return json.dumps(payload)

    def _clean_samples(self):
        for s in self.sensors:
            s['samples'] = []

    def _configure_sensors(self):
        GPIO.setmode(GPIO.BCM)

        self._set_all_shutdown_pins_to_low()
        self._create_sensor_instances()
        self._turn_on_sensors_one_by_one()
        self._clean_samples()

    def _turn_on_sensors_one_by_one(self):
        """Set shutdown pin high one after the other for all sensors"""
        for s in self.sensors:
            GPIO.output(s.get('shutdown_pin'), GPIO.HIGH)
            sleep(0.1)
            s.get('instance').start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

    def _create_sensor_instances(self):
        for s in self.sensors:
            s['instance'] = VL53L0X.VL53L0X(s.get('i2c_address'))

    def _set_all_shutdown_pins_to_low(self):
        """Set all shutdown pins low to turn off each sensor"""
        for s in self.sensors:
            GPIO.setup(s.get('shutdown_pin'), GPIO.OUT)
            GPIO.output(s.get('shutdown_pin'), GPIO.LOW)

        sleep(0.3)  # Make sure sensors have time to reset

    def _get_sampling_rate_ms(self):
        return self.sensors[0].get('instance').get_timing() / 1000.0

    def _stop_ranging(self):
        for s in self.sensors:
            s.get('instance').stop_ranging()
