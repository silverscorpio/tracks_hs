# write your code here
from cmdline import get_cmdline_args
from socket_init import socket_init


def main():
    inputs_cmdline = get_cmdline_args()
    server_data = (inputs_cmdline.ipaddress, inputs_cmdline.port)
    msg = inputs_cmdline.msg
    print(socket_init(server_info=server_data, msg_to_send=msg))


if __name__ == "__main__":
    main()
