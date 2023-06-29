import socket
import threading

host = '10.128.0.8'
port = 55555

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            if message.decode('ascii') == 'exit':
                remove_client(client)
                client.close()
                break
            broadcast(message)
            print("New message from " + message.decode('ascii'))
        except:
            # Removing And Closing Clients
            remove_client(client)
            client.close()
            break

# Removing Client From Lists
def remove_client(client):
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        nickname = nicknames[index]
        nicknames.remove(nickname)
        broadcast('{} left!'.format(nickname).encode('ascii'))

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

print("Server is listening...")
receive()
