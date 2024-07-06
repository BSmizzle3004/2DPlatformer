import sqlite3
import hashlib

def runsql(*args):
    conn = sqlite3.connect("../Map Builder/User_Data.db")
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()

    if len(args) == 1:
        cursor.execute(args[0])
    else:
        cursor.execute(args[0], args[1])

    conn.commit()
    return cursor.fetchall()

def authenticate_user(c):
    c.send("Username: ".encode())
    username = c.recv(1024).decode()
    c.send("Password: ".encode())
    password = c.recv(1024).decode()
    password = hashlib.sha256(password.encode()).hexdigest()

    query = "SELECT UserID FROM UserData WHERE Username = ? AND Password = ?"
    result = runsql(query, (username, password))
    if result:
        c.send("Login successful".encode())
        return result[0][0]  # Return UserID
    else:
        c.send("Login failed".encode())
        return None

def new_user(c):
    c.send("New username:  ".encode())
    new_username = c.recv(1024).decode()
    c.send("New password: ".encode())
    new_password = c.recv(1024).decode()
    new_password = hashlib.sha256(new_password.encode()).hexdigest()

    insert_username_password = """
        INSERT INTO UserData(Username,Password)
        VALUES(?,?)
    """

    runsql(insert_username_password, (new_username, new_password))
    c.send("User created successfully".encode())


# Create UserData table
create_table_user_data = """
    CREATE TABLE IF NOT EXISTS UserData (
        UserID INTEGER PRIMARY KEY,
        Username VARCHAR(255) NOT NULL,
        Password VARCHAR(255) NOT NULL
    )
"""

runsql(create_table_user_data)

create_table_maps = """
    CREATE TABLE IF NOT EXISTS maps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        map_data TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES UserData(UserID)
    )
"""

runsql(create_table_maps)
