from utils import (exit_cmd,
                   add_cmd,
                   back_cmd,
                   sanitize_input,
                   invalid_cmd,
                   unknown_cmd,
                   no_input,
                   pre_check_add_cmd_input,
                   get_all_students,
                   )

CMD_DICT = {
    "exit": exit_cmd,
    "add students": add_cmd,
    "back": back_cmd,
    "blank": no_input,
    "invalid": invalid_cmd,
    "unknown": unknown_cmd,
    "list": get_all_students
}


def main():
    print("Learning Progress Tracker")
    current_student_count = 0
    while True:
        # non-blank input
        if user_input := sanitize_input(input()):
            if user_input in CMD_DICT:
                match user_input:
                    case "exit":
                        CMD_DICT.get(user_input)()
                        break
                    case "add students":
                        print("Enter student credentials or 'back' to return")
                        while True:
                            creds_str = input()
                            if creds_str and creds_str != "back":
                                if pre_check_add_cmd_input(add_cmd_str=creds_str):
                                    cmd_status = CMD_DICT.get(user_input)(creds_str)
                                    if cmd_status:
                                        current_student_count += 1
                                    elif cmd_status is None:
                                        CMD_DICT.get("invalid")()
                                    else:
                                        continue
                                else:
                                    CMD_DICT.get("invalid")()
                                    continue
                            elif creds_str == "back":
                                print(f"Total {current_student_count} students have been added.")
                                break
                            else:
                                CMD_DICT.get("invalid")()

                    case "back":
                        print(f"Total {current_student_count} students have been added.")
                        CMD_DICT.get(user_input)()

                    case "list":
                        CMD_DICT.get(user_input)()
            else:
                CMD_DICT.get("unknown")()

        # blank input
        else:
            CMD_DICT.get("blank")()


if __name__ == '__main__':
    main()
