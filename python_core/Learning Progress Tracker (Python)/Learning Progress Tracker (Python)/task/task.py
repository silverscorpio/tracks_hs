from utils import exit_cmd, add_cmd, back_cmd, no_input, sanitize_input, unknown_cmd

CMD_DICT = {
    "exit": exit_cmd,
    "add students": add_cmd,
    "back": back_cmd,
    "blank": no_input,
    "unknown": unknown_cmd,
}


def main():
    print("Learning Progress Tracker")
    current_student_count = 0
    while True:
        raw_user_input = input()
        user_input = sanitize_input(usr_val=raw_user_input)
        if user_input:
            if user_input in CMD_DICT:
                CMD_DICT.get(user_input)()
            else:
                CMD_DICT.get("unknown")()
        else:
            CMD_DICT.get("blank")()


if __name__ == '__main__':
    main()
