"""
    client file for Client Server communication
    a client will try to connect with auth request to server
    using userid, passcode (inserted from matrix keypad on resberry pi)
    and auth request header and process further the chat session by look
    up request for user and starts a chat session.
"""
import socket
#importing socket module create sockets for
#receiving and sending bytes over network
import sys
#importing sys module for system i/o or exit functionality
from time import sleep
#importing time moddule for introducing delay and time functionality
import json
#importing json module data serialization and deserialization tool
import threading
#importing threading module use concurrent programming
import hashlib
#hashlib module for hashing passcodes


HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 12345


class Client:
    """
        A class to manage the client connection
    """
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
        self.connect()
                
    
    def connect(self):
        """
            A method to connect to the serer server
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((IP, PORT))
        self.authenticate()
        self.ask_for_client_address()


    def authenticate(self):
        """
            A method to autheticate to the server
            Returns True if authenticated else False
        """
        try:
            # Send name to find id in database
            name_header = f'{len(self.name):<{HEADER_LENGTH}}'.encode()
            self.client_socket.send(name_header + self.name.encode())
            # sending username to authenticate
            username_header = f"{len(self.username):<{HEADER_LENGTH}}".encode('utf-8')
            self.client_socket.send(username_header + self.username)
            # Sending password to authenticate
            password_header = f'{len(password):<{HEADER_LENGTH}}'.encode()
            self.client_socket.send(password_header + self.password)
        except Exception as e:
            print(f"Error {e}")

    def get_data_from_server(self, message):
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(message_header + message)
        sleep(0.1)
        new_socket_header = self.client_socket.recv(HEADER_LENGTH)
        if not len(new_socket_header):
            print("Connection closed by server")
            sys.exit()
        len_socket = int(new_socket_header.decode().strip())
        new_socket = self.client_socket.recv(len_socket).decode()
        if new_socket is not None:
            return new_socket
        return None
            

    def ask_for_client_address(self):
        """
            Requests server for the certain clients ip
        """
        try:
            while True:
                message = input(f"Enter person's name you want to communicate with : ")
                if message:
                    new_socket = self.get_data_from_server(message)
                    if new_socket is None:
                        continue
                    else:
                        print(new_socket)
        except Exception as e:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
            

if __name__ == '__main__':
    name = input("Name: ").title()
    username = input("Username: ").encode('utf-8')
    password = input("Password: ").encode()
    client = Client(name, username, password)
