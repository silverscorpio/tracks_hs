import re
import uuid
from pprint import pprint
from collections import defaultdict

STUDENT_DATA: defaultdict = defaultdict(dict)


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
    student_count: int = 0

    def __new__(cls, name, email):
        cls.student_count += 1
        return super().__new__(cls)

    def __init__(self, name, email):
        self.name: str = name
        self.email: str = email
        self.id: uuid = uuid.uuid1()

    def save_student(self) -> None:
        STUDENT_DATA[self.id] = {
            "name": self.name,
            "email": self.email
        }

    @staticmethod
    def total_students() -> int:
        return Student.student_count

    def __str__(self):
        return f"{self.id}: {self.name}"


class RegexParser:
    # TODO add the re.ASCII flag
    EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_\.]+@[a-zA-Z0-9_]+\.[a-z]{2,3}", flags=re.ASCII)
    NAME_REGEX = re.compile(r"[A-Za-z' -]+[ '-]{1}[A-Za-z' -]{2,}", flags=re.ASCII)

    def __init__(self):
        self.user_input: str
        self.input_type: str

    @staticmethod
    def process_regex(self, regex_type: str, input_str: str):
        match regex_type:
            case "name":
                return RegexParser.match_regex(template=RegexParser.NAME_REGEX, str_to_match=input_str)
            case "email":
                return RegexParser.match_regex(template=RegexParser.EMAIL_REGEX, str_to_match=input_str)
            case _:
                raise ValueError("Invalid input for Regex Parser")

    @staticmethod
    def match_regex(template, str_to_match) -> bool:
        match = re.match(template, str_to_match)
        if match:
            return True
        return False


if __name__ == '__main__':
    x = Student("panda", "chaku@gmail.com")
    y = Student("chu", "alpha@gmail.com")
    z = Student("werwer", "psider@gmail.com")
    x.save_student()
    y.save_student()
    z.save_student()
    print(Student.total_students())
    pprint(STUDENT_DATA, indent=2)
