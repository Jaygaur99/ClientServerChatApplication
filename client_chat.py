from threading import Thread
from time import sleep
import socket

PORT = 65000
IP = 'localhost'

class Ser(Thread):
    def __init__(self):
        super().__init__()
        self.address = (IP, PORT)
        self.is_on = True

    def initilize_socket(self, address):
        """
            Initlize a socket on port 8085 and start listening to clients request
        """ 
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(address)
        self.server_socket.listen()

    def send(self):
        try:
            while True:
                msg = input("Server: ")
                self.soc.send(msg.encode())
        except Exception as e:
            print(f"Error {e}")
        return

    def recv(self):
        try:
            while True:
                msg = self.soc.recv(1024).decode()
                print(f"Client: {msg}".rjust(50))
        except Exception as e:
            print(f"ERROR {e}")
        return


    def run(self):
        self.listen()
        send = Thread(target=self.send)
        recv = Thread(target=self.recv)
        try:
            send.start()
            recv.start()
        
            send.join()
            recv.join()
        except KeyboardInterrupt as e:
            self.soc.close()
            self.server_socket.close()
            return
        except Exception as e:
            print(f"Error, {e}")
        
        print("All conections are closed now")
        self.soc.close()
        self.server_socket.close()
        
    def listen(self):
        self.soc, self.soc_add = self.server_socket.accept()
        print(f"Starting to listen on {self.address}")



class Cli(Thread):
    def __init__(self):
        super().__init__()

    def initilize_socket(self, address):
        """
            Initlize a socket on port 8085 and start listening to clients request
        """ 
        self.address = address
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect(self.address)
        print(f"Connected to {self.address}")
    
    def send(self):
        try:
            while True:
                msg = input("Client: ")
                self.soc.send(msg.encode())
            return None
        except Exception as e:
            print(f"Error {e}")

    def recv(self):
        try:
            while True:
                msg = self.soc.recv(1024).decode()
                print(f"Client: {msg}".rjust(50))
            return None
        except Exception as e:
            print(f"ERROR {e}")

    def run(self):
        send = Thread(target=self.send)
        recv = Thread(target=self.recv)
        try:
            send.start()
            recv.start()
            send.join()
            recv.join()
        except KeyboardInterrupt as e:
            self.soc.close()
            return
        except Exception as e:
            print(f"Error, {e}")
        print("All conections are closed now")
        self.soc.close()


class ClientChat:
    """
        A class to connect to the client chatting session to other client
    """
    def __init__(self, address):
        self.ip = address.split(',')[0][2:-1]
        self.address = (self.ip, PORT)
        self.state = self.initilize_state()
        self.state_list = []
        self.add_states(Ser())
        self.add_states(Cli())

    def initilize_state(self):
        """A small method to initilize state of self.state"""
        state = None
        while True:
            try:
                state = int(input("1. Do you want to receive connection\n2. Do you want to request connection: "))
            except:
                print("Invalid Input! Try again")
                continue
            if state == 1:
                return 1
            elif state == 2:
                return 2
            print("Invalid Input! Try again")

    def add_states(self, state):
        """A method to add states to the state_list"""
        self.state_list.append(state)

    def start_chat_meet(self):
        """A method to start the chat session"""
        print(self.address, self.ip)
        self.state_list[self.state-1].initilize_socket(self.address)
        self.state_list[self.state-1].run()


if __name__ == "__main__":
    c =ClientChat(('127.0.0.1', 80))