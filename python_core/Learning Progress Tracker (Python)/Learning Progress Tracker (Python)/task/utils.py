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


def invalid_cmd():
    print("Incorrect credentials")


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

    def __new__(cls, first_name, last_name, email):
        cls.student_count += 1
        return super().__new__(cls)

    def __init__(self, first_name, last_name, email):
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.email: str = email
        self.id: uuid = uuid.uuid1()

    def save_student(self) -> None:
        STUDENT_DATA[self.id] = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }

    @staticmethod
    def total_students() -> int:
        return Student.student_count

    def __str__(self):
        return f"{self.id} - {self.first_name} {self.last_name}"


class InputParser:
    """
    extract the email (easier) from the input string and use the match to split and get the name
    """
    NAME_REGEX = re.compile(r"[A-Za-z' -]+[ '-]{1}[A-Za-z' -]{2,}", flags=re.ASCII)
    EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_\.]+@[a-zA-Z0-9_]+\.[a-z]{2,3}", flags=re.ASCII)

    def __init__(self):
        self._user_input = None
        self.email = None
        self.first_name = None
        self.last_name = None

    @property
    def user_input(self):
        return self._user_input

    @user_input.setter
    def user_input(self, user_input_val):
        self._user_input = user_input_val

    def extract_email(self) -> bool | tuple[str, tuple[int, int]]:
        match = re.search(InputParser.EMAIL_REGEX, self._user_input)
        if match:
            return match.group(), match.span()
        return False

    def process(self):
        if self._user_input:
            regex_return = self.extract_email()
            if regex_return:
                email, span_indices = regex_return
                self.email = email.strip()
                self.first_name, self.last_name = self._user_input[:span_indices(0)].split(maxsplit=1)
            else:
                print("No regex match")
        raise ValueError("User input string needs to be set first")

    def get_data(self) -> dict:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }


if __name__ == '__main__':
    x = Student("panda", "dodo", "chaku@gmail.com")
    y = Student("chu", "champi", "alpha@gmail.com")
    z = Student("werwer", "lulu", "psider@gmail.com")
    x.save_student()
    y.save_student()
    z.save_student()
    print(Student.total_students())
    pprint(STUDENT_DATA, indent=2)
