import sqlite3
from contextlib import contextmanager
import time



@contextmanager
def get_connection():
    connection = sqlite3.connect("ocean.db")
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Bot (admin TEXT NOT NULL, props TEXT NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY, username, xid INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Payments (date TEXT, id INTEGER, username TEXT, xid INTEGER, sum INTEGER, method TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Withdraws (date TEXT, id INTEGER, username TEXT, xid INTEGER, code INTEGER, method TEXT, props TEXT)''')

    # cursor.execute('INSERT OR IGNORE INTO Bot (admin, props) VALUES (?, ?)', ('ocean_sup', "996100200300"))
    try:
        yield cursor
        connection.commit() 
    finally:
        connection.close() 

def get_bot_data():
    with get_connection() as cursor:
        cursor.execute("SELECT admin, props FROM Bot LIMIT 1")
        row = cursor.fetchone()
        if row:
            return {"admin": row[0], "props": row[1]}
        else:
            return {"admin": None, "props": None}

def update_admin(new_admin):
    with get_connection() as cursor:
        cursor.execute("UPDATE Bot SET admin = ?", (new_admin,))

def update_props(new_props):
    with get_connection() as cursor:
        cursor.execute("UPDATE Bot set props = ?", (new_props,))
        
        

def get_user_data(id):
    with get_connection() as cursor:
        cursor.execute("SELECT xid FROM Users WHERE id = ?", (id,))
        result = cursor.fetchone()
        if not result:
         return None
        else:
         return result[0]

def get_username(id):
    with get_connection() as cursor:
        cursor.execute("SELECT username FROM Users WHERE id = ?", (id,))
        result = cursor.fetchone()
        if not result:
         return None
        else:
         return result[0]
        
def update_user(id: int, username: str, xid: int):
    with get_connection() as cursor:
        cursor.execute("SELECT xid FROM Users WHERE id = ?", (id,))
        result = cursor.fetchone()

        if not result:
            cursor.execute(
                "INSERT INTO Users (id, username, xid) VALUES (?, ?, ?)",
                (id, username, xid)
            )
        else:
            current_xid = result[0]
            if current_xid != xid:
                cursor.execute(
                    "UPDATE Users SET xid = ? WHERE id = ?",
                    (xid, id)
                )
                
                
                
def update_payment_history(user_id, username, xid, amount, method):
    with get_connection() as cursor:
        date = time.strftime("%d.%m.%Y-%H:%M")         
        cursor.execute("""INSERT INTO Payments (date, id, username, xid, sum, method) VALUES (?, ?, ?, ?, ?, ?)""", (date, user_id, username, xid, amount, method))

def update_withdraw_history(user_id, username, xid, code, method, props):
    with get_connection() as cursor:
        date = time.strftime("%d.%m.%Y-%H:%M")         
        cursor.execute("""INSERT INTO Withdraws (date, id, username, xid, code, method, props) VALUES (?, ?, ?, ?, ?, ?, ?)""", (date, user_id, username, xid, code, method, props))
                