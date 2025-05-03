import sqlite3
from contextlib import contextmanager




@contextmanager
def get_connection():
    connection = sqlite3.connect("ocean.db")
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Bot (admin TEXT NOT NULL, props TEXT NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY, username TEXT NOT NULL, xid INTEGER)''')

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