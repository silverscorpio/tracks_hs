from utils import (exit_cmd,
                   add_cmd,
                   back_cmd,
                   sanitize_input,
                   invalid_cmd,
                   unknown_cmd,
                   no_input,
                   pre_check_add_cmd_input,
                   get_all_students,
                   process_id_scores,
                   check_id,
                   get_student_data,
                   )

CMD_DICT = {
    "exit": exit_cmd,
    "add students": add_cmd,
    "back": back_cmd,
    "blank": no_input,
    "invalid": invalid_cmd,
    "unknown": unknown_cmd,
    "list": get_all_students,
    "add points": process_id_scores,
    "find": check_id,
    # "statistics": stats,
    "data": get_student_data,
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

                    case "add points":
                        print("Enter an id and points or 'back' to return")
                        while True:
                            id_scores_str = input()
                            if id_scores_str == "back":
                                break
                            CMD_DICT.get(user_input)(id_scores_str)

                    case "find":
                        print("Enter an id or 'back' to return.")
                        while True:
                            find_input_str = input()
                            if find_input_str == "back":
                                break
                            CMD_DICT.get(user_input)(find_input_str)

                    case "statistics":
                        print("Type the name of a course to see details or 'back' to quit")
                        while True:
                            CMD_DICT.get(user_input)()
                            subject = input()
                            if subject == "back":
                                break
                            elif subject not in ("Python", "DSA", "Databases", "Flask"):
                                print("Unknown course")
                            else:
                                subject_stats(subject)

                    case "data":
                        CMD_DICT.get(user_input)()

            else:
                CMD_DICT.get("unknown")()

        # blank input
        else:
            CMD_DICT.get("blank")()


if __name__ == '__main__':
    main()
