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
backup_folder = (BASE_FOLDER / "backup/").mkdir()


if __name__ == "__main__":
    logger.info("Connecting to database...")
    create_database()

    with open("settings.json", "r") as f:
        settings = json.loads(f.read())

    client = Client(settings["target_mac_address"], settings["target_port"], settings["target_ssid"], settings["target_password"])
    client.start()

    t = Thread(target=main_task)
    t.run()

    while True:
        files_not_sent = get_files_not_sent()
        
        for file in files_not_sent:
            path = Path(file)
            send_file(client.socket, filename=path.name)
            set_file_status(file, "sent")

        sleep(20)
