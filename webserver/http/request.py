from socket import socket
from typing import Generator, Dict
from webserver.util import ReturnValueGenerator


class BadRequestError(Exception):
    pass


class Request:
    def __init__(self, method: str, path: str,
                 headers: Dict[str, str] = None, body: bytes = None):
        self.method = method
        self.path = path
        self.headers = headers or {}
        self.body = body or b''

    @classmethod
    def from_socket(cls, client_socket: socket) -> 'Request':
        socket_generator = ReturnValueGenerator(
            Request.iter_socket(client_socket))
        first = True
        headers = {}
        method: str
        path: str
        for line in socket_generator:
            if first:
                method, path, _ = line.split()
                first = False
            else:
                key, value = line.split(':', 1)
                value = value.strip()
                headers[key] = value
        body = socket_generator.value
        return cls(method, path, headers, body)

    @staticmethod
    def iter_socket(client_socket: socket,
                    buffer_size: int = 1024) -> Generator[str, None, bytes]:
        data = bytes()
        while True:
            chunk = client_socket.recv(buffer_size)
            if not chunk:
                return b''
            data += chunk
            while True:
                try:
                    delimiter = data.index(b'\r\n')
                    line = data[:delimiter]
                    data = data[delimiter + 2:]
                    if not line:
                        return data[2:]
                    yield line.decode('ascii')
                except IndexError:
                    break

    def __bytes__(self) -> bytes:
        result = f'{self.method} {self.path} HTTP/1.1\r\n'
        for name, value in self.headers.items():
            result += f'{name}: {value}\r\n'
        result += '\r\n'
        result = result.encode('ascii')
        result += self.body
        return result
