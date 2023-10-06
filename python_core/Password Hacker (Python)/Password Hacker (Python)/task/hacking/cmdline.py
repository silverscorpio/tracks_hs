import argparse


def get_cmdline_args():
    parser = argparse.ArgumentParser(description="establishes socket connection")
    parser.add_argument("ipaddress", type=str, help="ip address of server")
    parser.add_argument("port", type=int, help="port")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    print(get_cmdline_args())
