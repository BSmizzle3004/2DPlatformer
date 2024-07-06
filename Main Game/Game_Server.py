import socket
import threading
import json

HOST = "127.0.0.1"
PORT = 50000

block_array = []
with open("../Map Builder/block_positions.txt", "r") as file:
    for line in file:
        block_array.append(line.strip().split())

Player1_pos = [700, 700]
Player2_pos = [800, 700]

def recv_from_client(connection, client_list):
    while True:
        data = connection.recv(1024)
        if not data:
            break
        else:
            data.decode()
            packet = json.loads(data)
            print(packet)
            for client in client_list:
                if client != connection:
                    try:
                        client.send(data)
                    except:
                        client_list.remove(client)

def main():
    client_list = []
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    print("Server is up and running on IP", HOST, "and port", PORT)
    server_running = True

    while server_running:
        connection, address = s.accept()
        client_list.append(connection)
        print("New connection found")
        threading.Thread(target=recv_from_client, args=(connection, client_list)).start()
        if len(client_list) == 2:
            packet = {"command": "SETUP", "map": block_array, "position1": Player1_pos, "position2": Player2_pos}
            client_list[0].send(json.dumps(packet).encode())
            packet = {"command": "SETUP", "map": block_array, "position1": Player2_pos, "position2": Player1_pos}
            client_list[1].send(json.dumps(packet).encode())

if __name__ == "__main__":
    main()