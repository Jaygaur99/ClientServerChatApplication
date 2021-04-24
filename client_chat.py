from threading import Thread
from time import sleep
import socket

PORT = 65000
IP = 'localhost'

class Ser(Thread):
    def __init__(self, name):
        super().__init__()
        self.is_on = True
        self.name = name

    def initilize_socket(self, address):
        """
            Initlize a socket on port 8085 and start listening to clients request
        """ 
        self.address = address
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(address)
        self.server_socket.listen()
    
    def send_name(self):
        name = f"{self.name}".encode()
        self.other_name = self.soc.recv(1024).decode()
        self.soc.send(name)
        
    def send(self):
        try:
            while True:
                msg = input(f"{self.name}: ")
                self.soc.send(msg.encode())
            return
        except:
            pass

    def recv(self):
        try:
            while True:
                msg = self.soc.recv(1024).decode()
                print(f"{self.other_name}: {msg}".rjust(50))
            return
        except:
            pass

    def run(self):
        self.listen()
        send = Thread(target=self.send)
        recv = Thread(target=self.recv)
        try:
            send.start()
            recv.start()
        
            send.join()
            recv.join()
        except KeyboardInterrupt:
            self.soc.close()
            self.server_socket.close()
            return
        except:
            print(f"Error, Your Friend Is Not online Anymore")
            self.soc.close()
            self.server_socket.close()
        print("All conections are closed now")
        self.soc.close()
        self.server_socket.close()
        
    def listen(self):
        print(f"Starting to listen on {self.address}")
        self.soc, self.soc_add = self.server_socket.accept()
        self.send_name()
        print(f"Connected to {self.address}")



class Cli(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def initilize_socket(self, address):
        """
            Initlize a socket on port 8085 and start listening to clients request
        """ 
        self.address = address
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect(self.address)
        self.send_name()
        print(f"Connected to {self.address}")
    
    def send_name(self):
        name = f"{self.name}".encode()
        self.soc.send(name)
        self.other_name = self.soc.recv(1024).decode()
    
    def send(self):
        try:
            while True:
                msg = input(f"{self.name}: ")
                self.soc.send(msg.encode())
            return None
        except:
            pass

    def recv(self):
        try:
            while True:
                msg = self.soc.recv(1024).decode()
                print(f"{self.other_name}: {msg}".rjust(50))
            return None
        except:
            pass

    def run(self):
        send = Thread(target=self.send)
        recv = Thread(target=self.recv)
        try:
            send.start()
            recv.start()
            send.join()
            recv.join()
        except KeyboardInterrupt:
            self.soc.close()
            return
        except:
            print(f"Error, Your Friend Is Not online Anymore")
            pass
        print("All conections are closed now")
        self.soc.close()


class ClientChat:
    """
        A class to connect to the client chatting session to other client
    """
    def __init__(self, address, name):
        self.name = name
        if address == False:
            self.ip = IP
            self.state = 2
        else:
            self.ip = address.split(',')[0][2:-1]
            self.state = 1
        self.address = (self.ip, PORT)
        self.state_list = []
        self.add_states(Ser(self.name))
        self.add_states(Cli(self.name))

    def add_states(self, state):
        """A method to add states to the state_list"""
        self.state_list.append(state)

    def start_chat_meet(self):
        """A method to start the chat session"""
        print(self.address, self.ip)
        self.state_list[self.state-1].initilize_socket(self.address)
        self.state_list[self.state-1].run()


if __name__ == "__main__":
    c =ClientChat(('127.0.0.1', 80), "Jay")