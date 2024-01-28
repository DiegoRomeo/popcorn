import json
from pathlib import Path
from threading import Thread
from time import sleep

import logzero

from client import Client
from task import main_task
from utils import *

BASE_FOLDER = Path(__file__)

logzero.logfile("client.log")
backup_folder = (BASE_FOLDER / "backup")


if __name__ == "__main__":
    logger.info("Connecting to database...")
    create_database()

    with open("settings.json", "r") as f:
        settings = json.loads(f.read())

    client = Client(settings["target_mac_address"], settings["target_port"], settings["target_ssid"], settings["target_password"])
    client.start()

    t = Thread(target=main_task)
    t.start()

    while True:
        files_not_sent = get_files_not_sent()
        
        for row in files_not_sent:
            path = Path(row[1])
            send_file(socket=client.socket, file_path=path)
            set_file_status(path, "sent")
            sleep(0.3)

        client.socket.send(b'')

        if client.socket.recv(1024) == B"Close connection":
            client.close()
            exit()

        sleep(15)
