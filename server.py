"""
    A Server Socket which listen for clients and process there request as
    if client has login request, userid and passcode log them in active users
    or if client request for lookup than send valid request if user is logged in
"""
import socket
import select
from data_base_handling import DataBaseHandling
from time import sleep

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 12345

class Server:
    """
        TCP IP server to accept and process client requests according to super
        secure communication protocols.
    """
    def __init__(self):
        self.data_base_handler = DataBaseHandling()
        self.initilize_socket()
        self.sockets_list = [self.server_socket]
        self.clients = {}
        print(f'Listening for connections on {IP}:{PORT}...')

    def initilize_socket(self):
        """
            Initlize a socket on port 8082 and start listning to clients request
        """ 
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((IP, PORT))
        self.server_socket.listen()


    def receive_message(self, c_socket):
        """
            A method to receive the message from from the client socket
        """
        try:
            message_header = c_socket.recv(HEADER_LENGTH)
            if not len(message_header):
                return False
            message_length = int(message_header.decode('utf-8').strip())
            return {'header': message_header, 'data': c_socket.recv(message_length).decode()}
        except:
            return False

    def add_to_server(self):
        """
            Add the connection to the server
        """
        self.client_socket, self.client_address = self.server_socket.accept()
        user = self.receive_message(self.client_socket)
        username = self.receive_message(self.client_socket)
        password = self.receive_message(self.client_socket)
        if user is False:
            return
        if self.data_base_handler.is_new(user['data']):
            self.data_base_handler.write_to_file(user["data"], username['data'], password['data'], self.client_address)
            print("request accepted")
        else:
            if not self.data_base_handler.validate_data(user["data"], username['data'], password['data']):
                self.client_socket.close()
                print("request denied")
            else:
                print("request accepted")

        self.sockets_list.append(self.client_socket)
        self.clients[self.client_socket] = [user['data'], self.client_address]
        print('Accepted new connection from {}:{}, username: {}'.format(*self.client_address,
                                                                        user['data']))

    def send_ip(self, notified_socket):
        """
            Send the IP address to the client.
        """
        sleep(0.2)
        message = self.receive_message(notified_socket)
        if message is False:
            return
        if message['data'] == 'close':
            print('Closed connection from: {}'.format(self.clients[notified_socket]))
            self.sockets_list.remove(notified_socket)
            del self.clients[notified_socket]
            return
        for _, name in self.clients.items():
            if name[0] == message['data']:
                send_soc = f"{name[1]}".encode()
                send_soc_header = f"{len(send_soc):<{HEADER_LENGTH}}".encode('utf-8')
                break
        else:
            send_soc = 'None'.encode()
            send_soc_header = f"{len(send_soc):<{HEADER_LENGTH}}".encode('utf-8')
        notified_socket.send(send_soc_header + send_soc)
        print("Data sent successfully")


    def accept(self):
        """
            will accept requests of client
        """
        self.read_sockets, _, self.exception_sockets = select.select(self.sockets_list, [], self.sockets_list)
        for notified_socket in self.read_sockets:
            if notified_socket == self.server_socket:
                self.add_to_server()
            else:
                self.send_ip(notified_socket)
        for notified_socket in self.exception_sockets:
            self.sockets_list.remove(notified_socket)
            del self.clients[notified_socket]

if __name__ == '__main__':
    server = Server()
    try:
        while True:
            server.accept()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    except Exception as e:
        print("ERROR: ",e)
