from serial.tools import list_ports

def enumerate_serial_devices():
    return set([item for item in list_ports.comports()])

def check_new_devices(old_devices):
    devices = enumerate_serial_devices()
    new_devices = devices.difference(old_devices)
