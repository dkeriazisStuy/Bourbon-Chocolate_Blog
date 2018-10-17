import sqlite3  # Enable control of an sqlite database
import csv  # Facilitates CSV I/O

DB_FILE = 'data.db'
if __name__ == "__main__":
    DB_FILE = '../data/' + DB_FILE

db = sqlite3.connect(DB_FILE)  # Open if file exists, otherwise create
c = db.cursor()  # Facilitate db operations

def create_table():
    try:
        c.execute('''CREATE TABLE users (
                username PRIMARY KEY TEXT,
                pass_hash BLOB,
                salt BLOB,
                karma INT
                )''')
    except:
        pass

def main():
    create_table()
    db.commit()  # Save changes
    db.close()  # Close database

if __name__ == "__main__":
    main()

