import platform
import subprocess

from logzero import logger, logfile
from pathlib import Path

logfile("../server.log")

def get_hotspot_ip_linux():
    result = subprocess.run(["ip", "addr", "show", "dev", "wlan0"], capture_output=True, text=True)
    ip_address = None

    for line in result.stdout.splitlines():
        if "inet " in line:
            ip_address = line.split()[1].split("/")[0]

    return ip_address

def get_hotspot_ip_windows():
    # Get the IP address of the connected WiFi network
    result = subprocess.run(["ipconfig"], capture_output=True, text=True)
    ip_address = None

    for line in result.stdout.splitlines():
        if "IPv4 Address" in line:
            ip_address = line.split(":")[1].strip()

    return ip_address

def get_hotspot_ip():
    os = platform.system()
    if os == "Windows":
        target_ip_address = get_hotspot_ip_windows()
    elif os == "Linux":
        target_ip_address = get_hotspot_ip_linux()
    else:
        logger.error("Unknown operative system.")
        exit()
    return target_ip_address

def receive_files(socket, backup_folder: Path):
    while True:
        file_info = socket.recv(1024).decode()
        if not file_info:
            return

        file_name, file_size = file_info.split(":")
        file_size = int(file_size)

        logger.info(f"Receiving file: {file_name} ({file_size} bytes)")

        file_path = backup_folder / file_name
        with open(str(file_path), 'wb') as file:
            remaining_bytes = file_size
            
            while remaining_bytes > 0:
                data = socket.recv(min(1024, remaining_bytes))

                if not data:
                    break

                file.write(data)
                remaining_bytes -= len(data)

            logger.info(f"File received: {file_name}")
