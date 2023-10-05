# write your code here
from cmdline import get_cmdline_args
import socket


def socket_init(server_info: tuple, msg_to_send: str) -> str:
    with socket.socket() as client_socket:
        client_socket.connect(server_info)
        client_socket.send(msg_to_send.encode())
        response_bytes = client_socket.recv(1024)
        return response_bytes.decode()


def main():
    inputs_cmdline = get_cmdline_args()
    server_data = (inputs_cmdline.ipaddress, inputs_cmdline.port)
    msg = inputs_cmdline.msg
    print(socket_init(server_info=server_data, msg_to_send=msg))


if __name__ == "__main__":
    main()
