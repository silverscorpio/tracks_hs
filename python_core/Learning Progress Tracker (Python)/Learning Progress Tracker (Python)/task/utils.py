import re


# funcs

def exit_cmd():
    print("Bye!")


def no_input():
    pass


def unknown_cmd():
    print("Unknown command!")


def add_cmd():
    print("Enter student credentials or 'back' to return")


def back_cmd():
    print("Enter 'exit' to exit the program.")


def check_blank_input(usr_val: str) -> bool:
    return True if usr_val.strip() else False


def sanitize_input(usr_val: str) -> str:
    return usr_val.strip()


# classes
class Student:
    pass


class RegexParser:
    EMAIL_REGEX = r"[a-zA-Z0-9_\.]+@[a-zA-Z0-9_]+\.[a-z]{2,3}"
    NAME_REGEX = ""

    def email_parser(self):
        pass

    def name_parser(self):
        pass
