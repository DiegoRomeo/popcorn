from pathlib import Path
import sqlite3
from logzero import logger, logfile

logfile("../client.log")

def create_database():
    connection = sqlite3.connect('file_database.db')
    cursor = connection.cursor()

    # Create a table to store file paths
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT UNIQUE,
            status TEXT
        )
    ''')

    connection.commit()
    connection.close()

def add_file(file_path: Path, status):
    connection = sqlite3.connect('file_database.db')
    cursor = connection.cursor()

    try:
        cursor.execute('INSERT INTO files (file_path, status) VALUES (?, ?)', (str(file_path), status))
        connection.commit()
        logger.info(f"File path '{file_path}' added to the database with status '{status}'.")
    except sqlite3.IntegrityError:
        logger.warning(f"File path '{file_path}' already exists in the database.")

    connection.close()

def is_file_in_database(file_path: Path):
    connection = sqlite3.connect('file_database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM files WHERE file_path = ?', (str(file_path),))
    result = cursor.fetchone()

    connection.close()

    return result is not None

def get_all_files():
    connection = sqlite3.connect('file_database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM files')
    files = cursor.fetchall()

    connection.close()

    return files

def get_files_not_sent():
    connection = sqlite3.connect('file_database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM files WHERE status = ?', ('not sent',))
    files = cursor.fetchall()

    connection.close()

    return files

def set_file_status(file_path: Path, new_status):
    connection = sqlite3.connect('file_database.db')
    cursor = connection.cursor()

    try:
        cursor.execute('UPDATE files SET status = ? WHERE file_path = ?', (new_status, str(file_path)))
        connection.commit()
        logger.info(f"Status for file path '{file_path}' set to '{new_status}'.")
    except sqlite3.Error as e:
        logger.error(f"Error updating status for file path '{file_path}': {e}")

    connection.close()
