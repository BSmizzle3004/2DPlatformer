import sqlite3
import hashlib
import socket
import threading

HOST = "127.0.0.1"
PORT = 50000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

def handle_connection(c):
    attempts = 0
    while attempts < 3:
        c.send("Enter 1 to login, enter 2 to create a new username and password: ".encode())
        user_choice = c.recv(1024).decode()

        if user_choice == '1':
            c.send("Username: ".encode())
            username = c.recv(1024).decode()
            c.send("Password: ".encode())
            password = c.recv(1024).decode()
            password = hashlib.sha256(password.encode()).hexdigest()

            conn = sqlite3.connect("../Map Builder/User_Data.db")
            cur = conn.cursor()

            cur.execute("SELECT * FROM UserData WHERE Username = ? AND Password = ?", (username, password))

            if cur.fetchone():
                c.send("Login successful".encode())
                break
            else:
                c.send("Login Failed. Please try again.".encode())
                attempts += 1

        elif user_choice == '2':
            from User_Data import new_user
            new_user(c)

    if attempts == 3:
        c.send("Maximum login attempts reached. Connection closed.".encode())
        c.close()


while True:
    client, addr = server.accept()
    threading.Thread(target=handle_connection, args=(client,)).start()
