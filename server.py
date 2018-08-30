#!/usr/bin/env python
from time import sleep

from threads.broadcast_thread import BroadcastThread
from threads.camera_thread import CameraThread
from threads.camera_websocket_thread import CameraWebSocketThread
from threads.http_server_thread import HTTPServerThread
from threads.distance_sensors_thread import DistanceSensorsThread
from threads.motion_sensors_thread import MotionSensorsThread
from threads.sensors_websocket_thread import SensorsWebSocketThread


def main():
    camera_thread = CameraThread()

    camera_websocket_thread = CameraWebSocketThread()
    sensors_websocket_thread = SensorsWebSocketThread()
    http_thread = HTTPServerThread()

    broadcast_thread = BroadcastThread(camera_thread.camera, camera_websocket_thread.server)

    distance_sensor_thread = DistanceSensorsThread(sensors_websocket_thread.server)
    motion_sensor_thread = MotionSensorsThread(sensors_websocket_thread.server)

    camera_thread.start_recording(broadcast_thread.output)

    try:
        print('Starting camera websocket thread')
        camera_websocket_thread.start()
        print('Starting sensors websocket thread')
        sensors_websocket_thread.start()
        print('Starting HTTP server thread')
        http_thread.start()
        print('Starting broadcast thread')
        broadcast_thread.start()
        print('Starting distance sensors thread')
        distance_sensor_thread.start()
        print('Starting motion sensors thread')
        motion_sensor_thread.start()
        print('Starting camera thread')
        camera_thread.start()

        # Infinite loop
        while True:
            sleep(5)

    except KeyboardInterrupt:
        pass
    finally:
        camera_thread.stop()
        camera_thread.join()

        broadcast_thread.stop()
        broadcast_thread.join()

        distance_sensor_thread.stop()
        distance_sensor_thread.join()

        motion_sensor_thread.stop()
        motion_sensor_thread.join()

        http_thread.stop()
        http_thread.join()

        camera_websocket_thread.stop()
        camera_websocket_thread.join()

        sensors_websocket_thread.stop()
        sensors_websocket_thread.join()


if __name__ == '__main__':
    main()
