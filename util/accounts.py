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

def start_db():
    db = sqlite3.connect(DB_FILE)  # Open if file exists, otherwise create
    c = db.cursor()  # Facilitate db operations
    return db, c

def end_db(db):
    db.commit()  # Save changes to database
    db.close()  # Close database

def create_table():
    db, c = start_db()
    try:
        c.execute('''CREATE TABLE users (
                    username TEXT PRIMARY KEY,
                    pass_hash BLOB,
                    salt BLOB,
                    karma INT
                )''')
    except sqlite3.OperationalError:  # Table already exists
        pass
    end_db(db)

def user_exists(username):
    db, c = start_db()
    # Check whether there is a row in 'users' where the column 'username' has
    # the value of `username`
    c.execute(
        'SELECT EXISTS(SELECT 1 FROM users WHERE username=? LIMIT 1)',
        (username,)
    )
    result = c.fetchone()[0]  # 1 if user exists, else 0
    end_db(db)
    return result == 1

def hash_pass(password, salt):
    return hashlib.pbkdf2_hmac('sha512', password.encode(), salt, 100000)

def get_salt():
    return os.urandom(32)

def add_user(username, password):
    db, c = start_db()
    salt = get_salt()
    pass_hash = hash_pass(password, salt)
    c.execute(
        'INSERT INTO users VALUES (?, ?, ?, 0)',
        (username, pass_hash, salt)
    )
    end_db(db)

def auth_user(username, password):  # Not yet implemented
    db, c = start_db()
    c.execute(
        'SELECT pass_hash, salt FROM users WHERE username=? LIMIT 1',
        (username,)
    )
    result = c.fetchone()  # 1 if user exists, else 0
    end_db(db)
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

def logout_user(session):
    del session['user']

def get_logged_in_user(session):
    return session['user']

def remove_user(username):
    db, c = start_db()
    c.execute(
        'DELETE FROM users WHERE username=?',
        (username,)
    )
    end_db(db)

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

