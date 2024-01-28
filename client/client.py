import platform
import socket

from logzero import logfile, logger

from utils import *

logfile("client.log")

class Client:

    def __init__(self, target_mac_address, target_port, target_ssid, target_password) -> None:
        self.target_mac_address = target_mac_address
        self.target_port = target_port
        self.target_ssid = target_ssid
        self.target_password = target_password
        
        self.os = platform.system()

    @property
    def target_ip_address(self):
        logger.info("Retrieving target ip address...")
        ip = get_connected_device_ip(self.target_mac_address)
        logger.info(f"target ip address: {ip}.")
        return ip

    def start(self):
        if self.os == "Linux":
            connect_to_wifi_linux(self.target_ssid, self.target_password)
        elif self.os == "Windows":
            connect_to_wifi_windows(self.target_ssid, self.target_password)

        logger.info("Creating client socket.")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.target_ip_address, self.target_port))

    def close(self):
        self.socket.close()
