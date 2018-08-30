#!/usr/bin/env python
from time import sleep

from threads.broadcast_thread import BroadcastThread
from threads.camera_thread import CameraThread
from threads.http_server_thread import HTTPServerThread
from threads.sensors_thread import SensorsThread
from threads.web_socket_thread import WebSocketThread


def main():
    camera_thread = CameraThread()
    websocket_thread = WebSocketThread()
    http_thread = HTTPServerThread()
    broadcast_thread = BroadcastThread(camera_thread.camera, websocket_thread.server)
    sensors_thread = SensorsThread(websocket_thread.server)
    camera_thread.start_recording(broadcast_thread.output)

    try:
        print('Starting websockets thread')
        websocket_thread.start()
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

        websocket_thread.stop()
        websocket_thread.join()


if __name__ == '__main__':
    main()
