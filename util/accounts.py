import sqlite3  # Enable control of an sqlite database
import csv  # Facilitates CSV I/O
import os
import hashlib
import hmac

import os.path  # Used for file locations
CUR_DIR = os.path.dirname(__file__)  # Absolute path to current directory
ROOT_DIR = os.path.join(CUR_DIR, os.path.pardir)  # Location of root directory
DATA_DIR = os.path.join(ROOT_DIR, 'data')  # Location of data directory
DB_FILE = os.path.join(DATA_DIR, 'data.db')  # Location of database file

db = sqlite3.connect(
        DB_FILE,  # Open if file exists, otherwise create
        check_same_thread=False  # Allow it to be used across files
)
c = db.cursor()  # Facilitate db operations

def create_table():
    try:
        c.execute('''CREATE TABLE users (
                    username TEXT PRIMARY KEY,
                    pass_hash BLOB,
                    salt BLOB,
                    karma INT
                )''')
    except sqlite3.OperationalError:  # Table already exists
        pass

def user_exists(username):
    # Check whether there is a row in 'users' where the column 'username' has
    # the value of `username`
    c.execute(
        'SELECT EXISTS(SELECT 1 FROM users WHERE username=? LIMIT 1)',
        (username,)
    )
    result = c.fetchone()[0]  # 1 if user exists, else 0
    return result == 1

def hash_pass(password, salt):
    return hashlib.pbkdf2_hmac('sha512', password.encode(), salt, 100000)

def get_salt():
    return os.urandom(32)

def add_user(username, password):
    salt = get_salt()
    pass_hash = hash_pass(password, salt)
    c.execute(
        'INSERT INTO users VALUES (?, ?, ?, 0)',
        (username, pass_hash, salt)
    )

def auth_user(username, password):  # Not yet implemented
    c.execute(
        'SELECT pass_hash, salt FROM users WHERE username=? LIMIT 1',
        (username,)
    )
    result = c.fetchone()  # 1 if user exists, else 0
    if result is None:
        return False

    pass_hash, salt = result
    if hmac.compare_digest(pass_hash, hash_pass(password, salt)):
        return True
    else:
        return False

def login_user(session, username):
    session['user'] = username

def is_logged_in(session):
    return 'user' in session

def remove_user(username):
    c.execute(
        'DELETE FROM users WHERE username=?',
        (username,)
    )

if __name__ == "__main__":
    create_table()

    print(user_exists('foo'), 'expected False')
    add_user('foo', 'bar')
    print(user_exists('foo'), 'expected True')

    print(auth_user('foo', 'bar'), 'expected True')
    print(auth_user('foo', 'bad_pass'), 'expected False')
    print(auth_user('not_a_user', 'bar'), 'expected False')
    print(auth_user('not_a_user', 'not_a_pass'), 'expected False')

    print(user_exists('foo'), 'expected True')
    remove_user('foo')
    print(user_exists('foo'), 'expected False')
    remove_user('foo')
    print(user_exists('foo'), 'expected False')

    print(user_exists('foo'), 'expected False')
    add_user('foo', 'bar')
    print(user_exists('foo'), 'expected True')

db.commit()  # Save changes to database
#  db.close()  # Close database

