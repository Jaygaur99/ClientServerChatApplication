import socket
import select
from data_base_handling import DataBaseHandling

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 12345
data_base_handler = DataBaseHandling()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()
sockets_list = [server_socket]
clients = {}
print(f'Listening for connections on {IP}:{PORT}...')


def receive_message(c_socket):
    # noinspection PyBroadException
    try:
        message_header = c_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': c_socket.recv(message_length).decode()}
    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)
            username = receive_message(client_socket)
            password = receive_message(client_socket)
            if user is False:
                continue
            if data_base_handler.is_new(user['data']):
                data_base_handler.write_to_file(user["data"], username['data'], password['data'], client_address)
                print("request accepted")
            else:
                if not data_base_handler.validate_data(user["data"], username['data'], password['data']):
                    client_socket.close()
                    print("request denied")
                    continue
                else:
                    print("request accepted")

            sockets_list.append(client_socket)
            clients[client_socket] = user['data']
            print('Accepted new connection from {}:{}, username: {}'.format(*client_address,
                                                                            user['data']))
        else:
            message = receive_message(notified_socket)
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]))
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            name_asking_user = clients[notified_socket]
            for soc, name in clients.items():
                if name == message['data']:
                    send_soc = f"{soc}".encode()
                    send_soc_header = f"{len(send_soc):<{HEADER_LENGTH}}".encode('utf-8')
                    break
            else:
                send_soc = 'None'.encode()
                send_soc_header = f"{len(send_soc):<{HEADER_LENGTH}}".encode('utf-8')
            notified_socket.send(send_soc_header + send_soc)
            print("Data sent successfully")

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
