import io
from http.server import HTTPServer, BaseHTTPRequestHandler
from string import Template
from threading import Thread
from time import time

import settings


class StreamingHttpHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
            return
        elif self.path == '/jsmpg.js':
            content_type = 'application/javascript'
            content = self.server.jsmpg_content
        elif self.path == '/client.js':
            content_type = 'application/javascript'
            content = self.server.client_content
        elif self.path == '/index.html':
            content_type = 'text/html; charset=utf-8'
            tpl = Template(self.server.index_template)
            content = tpl.safe_substitute(dict(
                CAMERA_WS_PORT=settings.CAMERA_WS_PORT,
                SENSORS_WS_PORT=settings.SENSORS_WS_PORT,
                WIDTH=settings.WIDTH, HEIGHT=settings.HEIGHT, COLOR=settings.COLOR,
                BGCOLOR=settings.BGCOLOR))
        else:
            self.send_error(404, 'File not found')
            return
        content = content.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', len(content))
        self.send_header('Last-Modified', self.date_time_string(time()))
        self.end_headers()
        if self.command == 'GET':
            self.wfile.write(content)


class StreamingHttpServer(HTTPServer):
    def __init__(self):
        super(StreamingHttpServer, self).__init__(
            ('', settings.HTTP_PORT), StreamingHttpHandler)
        with io.open('templates/index.html', 'r') as f:
            self.index_template = f.read()
        with io.open('assets/js/jsmpeg.js', 'r') as f:
            self.jsmpg_content = f.read()
        with io.open('assets/js/client.js', 'r') as f:
            self.client_content = f.read()


class HTTPServerThread(Thread):
    def __init__(self):
        print('Initializing HTTP server thread on port %d' % settings.HTTP_PORT)

        self.http_server = StreamingHttpServer()

        super(HTTPServerThread, self).__init__(target=self.http_server.serve_forever)

    def stop(self):
        print('Shutting down HTTP server ... ')

        self.http_server.shutdown()
