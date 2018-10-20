import os.path  # Used for file locations
import sqlite3

CUR_DIR = os.path.dirname(__file__)  # Absolute path to current directory
ROOT_DIR = os.path.join(CUR_DIR, os.path.pardir)  # Location of root directory
DATA_DIR = os.path.join(ROOT_DIR, 'data')  # Location of data directory
DB_FILE = os.path.join(DATA_DIR, 'data.db')  # Location of database file


def use_test_db():
    global DB_FILE
    DB_FILE = os.path.join(DATA_DIR, 'test.db')  # Use test database file


def start_db():
    db = sqlite3.connect(DB_FILE)  # Open if file exists, otherwise create
    c = db.cursor()  # Facilitate db operations
    return db, c


def end_db(db):
    db.commit()  # Save changes to database
    db.close()  # Close database

