__author__ = 'jkordas'
#module to handle connection to database

import sqlite3 as lite
import sys

DATABASE_NAME = "users.db"


def create_table():
    """
    creates USERS table if it not exist
    USERS: (login: username, password: hashed_password, salt: generated_salt_unique_value)
    """
    try:
        conn = lite.connect(DATABASE_NAME)

        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS USERS (login TEXT PRIMARY KEY, password TEXT, salt TEXT);')
        print "Table created successfully"

    except lite.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:
        if conn:
            conn.commit()
            conn.close()


def create_user(username, password, salt):
    """
    insert user into USERS table in database
    """
    try:
        conn = lite.connect(DATABASE_NAME)

        cur = conn.cursor()
        cur.execute('INSERT INTO USERS (login, password, salt) values (?, ?, ?)', (username, password, salt))
        print "User created successfully"

    except lite.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:
        if conn:
            conn.commit()
            conn.close()


def delete_user(username):
    """
    removes user from USERS table in database
    """
    try:
        conn = lite.connect(DATABASE_NAME)

        cur = conn.cursor()
        cur.execute('DELETE from USERS where login = ?', (username, ))
        print "User deleted successfully"

    except lite.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:
        if conn:
            conn.commit()
            conn.close()


def change_password(username, new_password, new_salt):
    """
    change password and salt for user into USERS table in database
    """
    try:
        conn = lite.connect(DATABASE_NAME)

        cur = conn.cursor()
        cur.execute('UPDATE USERS set password = ?, salt = ? where login = ?', (new_password, new_salt, username))

        print "Password changed successfully"

    except lite.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:
        if conn:
            conn.commit()
            conn.close()

def get_users():
    """
    prints all users form USERS table in database
    to test if everything was saved correctly
    """
    try:
        conn = lite.connect(DATABASE_NAME)

        cur = conn.cursor()
        result = cur.execute("SELECT login, password, salt from USERS")

        for row in result:
            print "username = ", row[0]
            print "password = ", row[1]
            print "salt = ", row[2] + "\n"

    except lite.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:
        if conn:
            conn.commit()
            conn.close()


def get_user(username):
    """
    returns row in database for given username (login)
    if user does not exist returns None
    """
    try:
        conn = lite.connect(DATABASE_NAME)

        cur = conn.cursor()
        result = cur.execute("SELECT * FROM USERS WHERE login = ?", (username, ))

        return result.fetchone()

    except lite.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:
        if conn:
            conn.close()


def get_password(username):
    """
    returns tuple (password, salt) for given username from database
    if username does not exist returns None
    """
    user = get_user(username)
    if user is not None:
        return (user[1], user[2])   #return (password , salt)
    else:
        return None


def is_username_taken(username):
    """
    checks if given username is already taken
    returns True if taken, False otherwise
    """

    try:
        conn = lite.connect(DATABASE_NAME)

        cur = conn.cursor()
        result = cur.execute("SELECT * FROM USERS WHERE login = ?", (username, ))

        return len(list(result)) > 0

    except lite.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:
        if conn:
            conn.close()