import sqlite3  # Enable control of an sqlite database
import csv  # Facilitates CSV I/O
import os
import hashlib
import hmac
import util.config as config


def create_table():
    db, c = config.start_db()
    try:
        c.execute('''CREATE TABLE users (
                    username TEXT PRIMARY KEY,
                    pass_hash BLOB NOT NULL,
                    salt BLOB NOT NULL,
                    karma INT NOT NULL
                )''')
    except sqlite3.OperationalError:  # Table already exists
        pass
    config.end_db(db)


def user_exists(username):
    db, c = config.start_db()
    # Check whether there is a row in 'users' where the column 'username' has
    # the value of `username`
    c.execute(
        'SELECT EXISTS(SELECT 1 FROM users WHERE username=? LIMIT 1)',
        (username,)
    )
    result = c.fetchone()[0]  # 1 if user exists, else 0
    config.end_db(db)
    return result == 1


def hash_pass(password, salt):
    return hashlib.pbkdf2_hmac('sha512', password.encode(), salt, 100000)


def get_salt():
    return os.urandom(32)


def valid_username(username):
    if username is None:  # SQLite integrity check
        return False
    if len(username) > 32:  # Arbitrary length cap
        return False
    if len(username) < 1:  # Not-as-arbitrary length minimum
        return False
    for i in username:
        if i not in config.CHARSET:
            return False
    return True


def valid_password(password):
    if password is None:  # SQLite integrity check
        return False
    if len(password) < 8:  # Arbitrary length minimum
        return False
    return True


def add_user(username, password):
    db, c = config.start_db()
    if not valid_username(username):
        return False
    if not valid_password(password):
        return False
    salt = get_salt()
    pass_hash = hash_pass(password, salt)
    c.execute(
        'INSERT INTO users VALUES (?, ?, ?, 0)',
        (username, pass_hash, salt)
    )
    config.end_db(db)
    return True


def auth_user(username, password):  # Not yet implemented
    db, c = config.start_db()
    c.execute(
        'SELECT pass_hash, salt FROM users WHERE username=? LIMIT 1',
        (username,)
    )
    result = c.fetchone()
    config.end_db(db)
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
    db, c = config.start_db()
    c.execute(
        'DELETE FROM users WHERE username=?',
        (username,)
    )
    config.end_db(db)

