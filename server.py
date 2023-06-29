#!/bin/python3
import socket
import threading
import subprocess


# Connection Data
host = '10.128.0.8'
# host = '192.168.0.192'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients


def broadcast(message):
    for client in clients:
        client.send(message)

# Ping Check


def ping_check(ip):
    command = ['ping', '-c', '4', ip]
    try:
        output = subprocess.check_output(
            command, timeout=5, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        return str(e.output)
    except subprocess.TimeoutExpired:
        return "Ping timeout"

# Handling Messages From Clients


def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            if message:
                broadcast(message)
                print("New message from " + message.decode('ascii'))
        except ConnectionResetError:
            # Connection Reset by Peer (client disconnected)
            break
        except Exception as e:
            print("Error occurred in handle:", e)
            break

    # Removing And Closing Client
    index = clients.index(client)
    clients.remove(client)
    client.close()
    nickname = nicknames[index]
    broadcast('{} left!'.format(nickname).encode('ascii'))
    nicknames.remove(nickname)

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

        # Print Nickname
        print("User {} connected".format(nickname))

        # Ping Check
        ping_result = ping_check(address[0])
        print("Ping result for {}: {}".format(address[0], ping_result))

        # Broadcast
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server if listening...")
receive()
