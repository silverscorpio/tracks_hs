import socket
from cmdline import get_cmdline_args
from pwd_combi import get_pwd_iterator, get_elements_list


def main():
    inputs_cmdline = get_cmdline_args()
    server_data = (inputs_cmdline.ipaddress, inputs_cmdline.port)
    with socket.socket() as client_socket:
        client_socket.connect(server_data)
        for i in range(1, len(all_elements) + 1):
            pwd_iter = get_pwd_iterator(iterator=all_elements, n=i)
            for j in pwd_iter:
                client_socket.send(''.join(j).encode())
                response_bytes = client_socket.recv(1024)
                if response_bytes.decode() == "Connection success!":
                    return ''.join(j)


if __name__ == "__main__":
    all_elements = get_elements_list()
    print(main())
