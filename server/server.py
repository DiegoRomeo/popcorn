import socket

from logzero import logfile, logger

logfile("server.log")

class Server:

    def __init__(self, target_ip_address, target_port) -> None:
        self.target_ip_address = target_ip_address
        self.target_port = target_port

    def start(self):
        logger.info("Cretaing server socket...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.target_ip_address, self.target_port))
        logger.info("Listening for connections...")
        self.socket.listen(1)
        self.client_socket, self.client_address = self.socket.accept()
    
    def close(self):
        self.socket.close()
