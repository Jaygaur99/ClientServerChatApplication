import socket
import sys
from time import sleep


HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 12345

name = input("Name: ").title()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)
name_header = f'{len(name):<{HEADER_LENGTH}}'.encode()
client_socket.send(name_header + name.encode())
username = input("Username: ").encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)
password = input("Password: ").encode()
password_header = f'{len(password):<{HEADER_LENGTH}}'.encode()
client_socket.send(password_header + password)
try:
    while True:
        message = input(f"Enter person's name you want to communicate with : ")
        if message:
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(message_header + message)
            sleep(0.5)
            new_socket_header = client_socket.recv(HEADER_LENGTH)
            if not len(new_socket_header):
                print("Connection closed by server")
                sys.exit()
            len_socket = int(new_socket_header.decode().strip())
            new_socket = client_socket.recv(len_socket).decode()
            if new_socket is not None:
                break
except Exception as e:
    print('Reading error: {}'.format(str(e)))
    sys.exit()
else:
    print(new_socket)
