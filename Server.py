import socket
import threading

HOST = '192.168.100.8'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.listen()

clients_array = []
nicks = []

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicks[clients_array.index(client)]}")
            broadcast(message)
        except:
            index = clients_array.index(client)
            clients_array.remove(client)
            client.close()
            nickname = nicks[index]
            nicks.remove(nickname)


def broadcast(msg):
    for client in clients_array:
        client.send(msg)

def receive():
    while True:
        client, address = server.accept()
        print(f"{str(address)} Connected!")

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)
        nicks.append(nickname)
        clients_array.append(client)

        print(f"{nickname} is the client")
        broadcast(f"{nickname} is now connected!\n".encode('utf-8'))
        client.send("Connected to server".encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server running")
receive()
