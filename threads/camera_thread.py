from threading import Thread
from time import sleep

import picamera

import settings


class CameraThread(Thread):
    def __init__(self):
        super().__init__()

        print('Initializing camera thread')

        self.camera = picamera.PiCamera()
        self.camera.resolution = (settings.WIDTH, settings.HEIGHT)
        self.camera.framerate = settings.FRAMERATE
        self.camera.vflip = settings.VFLIP  # flips image rightside up, as needed
        self.camera.hflip = settings.HFLIP  # flips image left-right, as needed
        sleep(1)  # camera warm-up time

        self.should_run = True

    def start_recording(self, output):
        print('Starting recording')

        self.camera.start_recording(output, 'yuv')

    def run(self):
        while self.should_run:
            self.camera.wait_recording(1)

    def stop(self):
        print('Finishing camera thread ...')
        self.should_run = False

        print('Stopping recording')
        self.camera.stop_recording()
        self.camera.close()
