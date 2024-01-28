from pathlib import Path
import subprocess
import time

from logzero import logfile, logger

logfile("../client.log")


def send_file(socket, file_path: Path):
    file_name = file_path.name
    file_size = file_path.stat().st_size
    file_info = f"{file_name}:{file_size}"

    socket.send(file_info.encode())
    
    time.sleep(0.2)
    with open(file_path, 'rb') as file:
        for data in iter(lambda: file.read(1024), b''):
            socket.send(data)

def connect_to_wifi_linux(ssid, password):
    # Disconnect from any existing WiFi network
    subprocess.run(["nmcli", "dev", "disconnect", "wlan0"])

    # Add a new connection with the provided SSID and password
    subprocess.run(["nmcli", "dev", "wifi", "connect", ssid, "password", password])

    # Wait for the connection to establish (you might need to adjust the sleep duration)
    time.sleep(5)

def connect_to_wifi_windows(ssid, password):
    # Disconnect from any existing WiFi network
    subprocess.run(["netsh", "interface", "set", "interface", "name='Wi-Fi'", "admin=disable"])

    # Connect to the specified WiFi network
    subprocess.run(["netsh", "interface", "set", "interface", "name='Wi-Fi'", "admin=enable"])
    subprocess.run(["netsh", "wlan", "connect", "name", f"'{ssid}'", "ssid", f"'{ssid}'", "interface='Wi-Fi'"])

    # Wait for the connection to establish (you might need to adjust the sleep duration)
    time.sleep(10)

    # Provide the password for the WiFi network
    subprocess.run(["netsh", "wlan", "add", "profileparameter", "user", "interface='Wi-Fi'", "name", f"'{ssid}'", "authentication=WPA2PSK"])
    subprocess.run(["netsh", "wlan", "set", "profileparameter", "user", "interface='Wi-Fi'", "name", f"'{ssid}'", "keyMaterial", f"'{password}'"])

    # Connect to the WiFi network
    subprocess.run(["netsh", "wlan", "connect", "name", f"'{ssid}'", "interface='Wi-Fi'"])

def get_connected_device_ip(mac_address):
    
    result = subprocess.check_output(["arp", "-a"], universal_newlines=True)

    for line in result.split("\n"):
        if "wlan0" in line and mac_address in line:
            ip_address = line.split(" ")[1][1:-1]
            return ip_address
    logger.error("Device not found.")
    exit()
