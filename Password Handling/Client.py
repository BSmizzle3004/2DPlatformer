import socket

HOST = "127.0.0.1"
PORT = 50000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

attempts = 0

while attempts < 3:
    user_choice = client.recv(1024).decode()
    choice = input(user_choice)
    client.send(choice.encode())

    username_prompt = client.recv(1024).decode()
    username = input(username_prompt)
    client.send(username.encode())

    password_prompt = client.recv(1024).decode()
    password = input(password_prompt)
    client.send(password.encode())

    msg = client.recv(1024).decode()
    print(msg)

    if msg == "Login successful":
        break
    else:
        attempts += 1

if attempts == 3:
    print("Maximum login attempts reached.")

client.close()
