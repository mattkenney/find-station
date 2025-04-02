#!/usr/bin/env python3
"""
Local development HTTP server for the find-station feature.
"""

import logging
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from json import dumps

from pythonjsonlogger.json import JsonFormatter

logFormat = '\x1b[34m%(asctime)s %(levelname)s %(message)s\x1b[39m'
logging.basicConfig(format=logFormat, level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger()
logHandler = logging.StreamHandler()
logHandler.setFormatter(JsonFormatter())
logger.addHandler(logHandler)

from request_handler import find_closest_station


class DevServerRequestHandler(BaseHTTPRequestHandler):
    """HTTPRequestHandler for local development"""
    def do_GET(self):
        payload = find_closest_station(self.command, self.path)
        self.send_response(payload.get('statusCode', 200))
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(dumps(payload).encode('utf-8'))


def run_server(port=8080):
    try:
        server_address = ('', port)
        httpd = HTTPServer(server_address, DevServerRequestHandler)
        logger.info(f"Server running at http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    run_server()
