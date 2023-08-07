import argparse


def get_cmdline_args():
    parser = argparse.ArgumentParser(description="establishes socket connection")
    parser.add_argument("--ipaddress")
    parser.add_argument("--port")
    parser.add_argument("--msg")


if __name__ == "__main__":
    get_cmdline_args()
