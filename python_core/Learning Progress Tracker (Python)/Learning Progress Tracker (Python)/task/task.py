from utils import exit_cmd, add_cmd, back_cmd, no_input

STUDENT_DATA = {}

CMD_DICT = {
    "exit": exit_cmd,
    "add students": add_cmd,
    "back": back_cmd,
    "no_input": no_input,
}


def main():
    print("Learning Progress Tracker")
    while True:
        user_input = input()
        if user_input in CMD_DICT:
            CMD_DICT.get(user_input)()
        else:
            if not user_input:
                CMD_DICT.get("no_input")()
            else:
                print("Unknown command!")


if __name__ == '__main__':
    main()
