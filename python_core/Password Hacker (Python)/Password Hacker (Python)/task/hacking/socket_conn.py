import socket


# function for stage 2 where the socket connection was used with a msg
def socket_conn(server_info: tuple, msg_to_send=None) -> str:
    with socket.socket() as client_socket:
        client_socket.connect(server_info)
        if msg_to_send is not None:
            client_socket.send(msg_to_send.encode())
            response_bytes = client_socket.recv(1024)
            return response_bytes.decode()


def socket_operation(socket_connection: socket, msg_to_send: str) -> str:
    socket_connection.send(msg_to_send.encode())
    response_bytes = socket_connection.recv(1024)
    return response_bytes.decode()
