from socket import socket
from typing import Callable, Dict
import logging

from webserver.http.response import Response
from webserver.http.request import Request
from webserver.tcp.server import Server


class HTTPServer(Server):
    def __init__(self, host: str = 'localhost', port: int = 5000):
        super().__init__(host, port)
        self.routes: Dict[str, Callable[[Request], Response]] = {}

    def handle_connection(self, client_socket: socket, client_address):
        request = Request.from_socket(client_socket)
        try:
            logging.debug(f'handling request for path {request.path}')
            response = self.routes[request.path](request)
        except KeyError:
            logging.error(f'no route for path {request.path}')
            body = b'Bad Gateway'
            headers = {
                'Content-Type': 'text/plain',
                'Content-Length': len(body)
            }
            response = Response(502, headers=headers, body=body)
        with client_socket:
            client_socket.sendall(bytes(response))

    def route(self, route: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.routes[route] = func
            return func
        return decorator
