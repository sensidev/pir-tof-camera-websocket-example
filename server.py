#!/usr/bin/env python
from time import sleep

from threads.broadcast_thread import BroadcastThread
from threads.camera_thread import CameraThread
from threads.camera_websocket_thread import CameraWebSocketThread
from threads.http_server_thread import HTTPServerThread
from threads.sensors_thread import SensorsThread
from threads.sensors_websocket_thread import SensorsWebSocketThread


def main():
    camera_thread = CameraThread()

    camera_websocket_thread = CameraWebSocketThread()
    sensors_websocket_thread = SensorsWebSocketThread()
    http_thread = HTTPServerThread()

    broadcast_thread = BroadcastThread(camera_thread.camera, camera_websocket_thread.server)
    sensors_thread = SensorsThread(sensors_websocket_thread.server)

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
        print('Starting sensors thread')
        sensors_thread.start()
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

        sensors_thread.stop()
        sensors_thread.join()

        http_thread.stop()
        http_thread.join()

        camera_websocket_thread.stop()
        camera_websocket_thread.join()

        sensors_websocket_thread.stop()
        sensors_websocket_thread.join()


if __name__ == '__main__':
    main()
