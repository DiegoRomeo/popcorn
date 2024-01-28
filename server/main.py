import json
import platform
from pathlib import Path

from logzero import logfile, logger

from .server import Server
from .utils import *

from time import sleep


base_folder = Path(__file__)
log_file = base_folder / "server.log"
settings_file = base_folder / "settings.json"
backup_folder = base_folder / "backup"

logfile(str(log_file))
secret = json.loads(open(str(settings_file), "r").read())

if __name__ == "__main__":
    if not backup_folder.is_dir():
        backup_folder.mkdir()
        logger.info("Local backup folder created.")

    target_ip_address = "0.0.0.0"
    logger.info(f"Target IP address: {target_ip_address}")
    
    logger.info("Creating server.")
    server = Server(target_ip_address, secret["target_port"])
    server.start()

    while True:
        receive_files(server.socket, backup_folder)
        logger.warning("File stream finished")
        keep_receiving = input("Do you want to keep listening for new files? [y/n]")
        while keep_receiving not in ["y", "n"]:
            keep_receiving = input("Do you want to keep listening for new files? [y/n]")
        if keep_receiving == "n":
            logger.info("Closing...")
            server.socket.send(b"Close connection")
            server.close()
            exit()
