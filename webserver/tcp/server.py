import socket
import logging


class Server:
    def __init__(self, host: str = 'localhost', port: int = 5000):
        self.host = host
        self.port = port

    def serve(self):
        with socket.socket() as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(0)
            logging.debug(f'listening on {self.host}:{self.port}')
            while True:
                client_socket, client_address = server_socket.accept()
                logging.debug(f'connection from {client_address}')
                self.handle_connection(client_socket, client_address)

    def handle_connection(self, client_socket: socket.socket, client_address):
        pass
