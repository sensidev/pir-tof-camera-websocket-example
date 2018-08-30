from threading import Thread
from wsgiref.simple_server import make_server

from ws4py.server.wsgirefserver import (
    WSGIServer,
    WebSocketWSGIHandler,
    WebSocketWSGIRequestHandler,
)
from ws4py.server.wsgiutils import WebSocketWSGIApplication
from ws4py.websocket import WebSocket

import settings


class SensorsWebSocketThread(Thread):
    def __init__(self):
        print('Initializing sensors websockets server on port %d' % settings.SENSORS_WS_PORT)

        WebSocketWSGIHandler.http_version = '1.1'

        self.websocket_server = make_server(
            '', settings.SENSORS_WS_PORT,
            server_class=WSGIServer,
            handler_class=WebSocketWSGIRequestHandler,
            app=WebSocketWSGIApplication(handler_cls=WebSocket))

        self.websocket_server.initialize_websockets_manager()

        super(SensorsWebSocketThread, self).__init__(target=self.websocket_server.serve_forever)

    @property
    def server(self):
        return self.websocket_server

    def stop(self):
        print('Shutting down sensors websockets server ...')

        self.websocket_server.shutdown()
