from utils import (exit_cmd,
                   add_cmd,
                   back_cmd,
                   sanitize_input,
                   invalid_cmd,
                   unknown_cmd,
                   no_input
                   )

CMD_DICT = {
    "exit": exit_cmd,
    "add students": add_cmd,
    "back": back_cmd,
    "blank": no_input,
    "invalid": invalid_cmd,
    "unknown": unknown_cmd,
}


def main():
    print("Learning Progress Tracker")
    current_student_count = 0
    while True:
        raw_user_input = input()
        user_input = sanitize_input(usr_val=raw_user_input)

        # non-blank input
        if user_input:
            if user_input in CMD_DICT:
                match user_input:
                    case "exit":
                        CMD_DICT.get(user_input)()
                        break
                    case "add students":
                        print("Enter student credentials or 'back' to return")
                        creds = input()
                        if creds != "back":
                            cmd_status = CMD_DICT.get(user_input)(creds)
                            if cmd_status:
                                current_student_count += 1
                            else:
                                CMD_DICT.get("invalid")()
                        elif creds == "back":
                            continue
                    case "back":
                        if current_student_count > 1:
                            print(f"Total {current_student_count} students have been added.")
                        else:
                            CMD_DICT.get(user_input)()

            else:
                CMD_DICT.get("unknown")()

        # blank input
        elif not user_input:
            CMD_DICT.get("blank")()


if __name__ == '__main__':
    main()
