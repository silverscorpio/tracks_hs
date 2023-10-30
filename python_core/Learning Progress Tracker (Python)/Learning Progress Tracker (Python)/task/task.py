from utils import exit_cmd, add_cmd, back_cmd, no_input, sanitize_input

STUDENT_DATA = {}
CMD_DICT = {
    "exit": exit_cmd,
    "add students": add_cmd,
    "back": back_cmd,
    "blank": no_input,
}


def main():
    print("Learning Progress Tracker")
    while True:
        raw_user_input = input()
        user_input = sanitize_input(usr_val=raw_user_input)
        if user_input:
            if user_input in CMD_DICT:
                CMD_DICT.get(user_input)()
        else:
            CMD_DICT.get("blank")()


if __name__ == '__main__':
    main()
