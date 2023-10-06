import socket


def socket_init(server_info: tuple, msg_to_send: str) -> str:
    with socket.socket() as client_socket:
        client_socket.connect(server_info)
        client_socket.send(msg_to_send.encode())
        response_bytes = client_socket.recv(1024)
        return response_bytes.decode()
