import re
from re import Pattern
import uuid
from pprint import pprint
from collections import defaultdict

STUDENT_DATA: defaultdict = defaultdict(dict)
STUDENT_ID_MAPPER: defaultdict = defaultdict(uuid.uuid1)


# funcs
def exit_cmd():
    print("Bye!")


def add_cmd(creds: str):
    # regex stuff
    parser_obj = InputParser()
    parser_obj.user_input = creds
    parser_obj.process()
    eval_result = parser_obj.evaluate_fields()
    if eval_result is None:
        return
    elif eval_result:
        # get parsed info
        student_data: dict = parser_obj.get_data()
        student = Student(**student_data)
        student.save_student()
        # pprint(STUDENT_DATA, indent=2)
        return True
    return False


def back_cmd():
    print("Enter 'exit' to exit the program.")


def unknown_cmd():
    print("Unknown command!")


def no_input():
    print("No input")


def invalid_cmd():
    print("Incorrect credentials.")


def sanitize_input(usr_val: str) -> str:
    return usr_val.strip()


def pre_check_add_cmd_input(add_cmd_str: str) -> bool:
    return True if len(add_cmd_str.split()) >= 3 else False


# classes
class Student:
    student_count: int = 0

    def __new__(cls, student_id, first_name, last_name, email):
        cls.student_count += 1
        return super().__new__(cls)

    def __init__(self, student_id, first_name, last_name, email):
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.email: str = email
        self.student_id: int = student_id
        self.total_score = 0
        self.map_id_uuid()

    def map_id_uuid(self):
        STUDENT_ID_MAPPER[self.student_id] = uuid.uuid1()

    def get_uuid_from_id(self):
        return STUDENT_ID_MAPPER[self.student_id]

    def save_student(self) -> None:
        STUDENT_DATA[self.get_uuid_from_id()] = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }
        print("The student has been added.")

    @staticmethod
    def total_students() -> int:
        return Student.student_count

    def __str__(self):
        return f"{self.get_uuid_from_id()} - {self.first_name} {self.last_name}"


class InputParser:
    """
    extract the email (easier) from the input string and use the match to split and get the name
    """

    FIRST_NAME_REGEX = re.compile(r"^(?![-'])(?:(([A-Za-z])|((['-])(?![-'])))){2,}\b[^-']", flags=re.ASCII)
    LAST_NAME_REGEX = re.compile(r" (?![-'])(?:(([A-Za-z])|((['-])(?![-'])))){2,}\b[^'-]$", flags=re.ASCII)
    EMAIL_REGEX = re.compile(r" (?:[a-zA-Z0-9_\.])+@(?:[a-zA-Z0-9_]+\.[a-z0-9]{1,3})", flags=re.ASCII)

    def __init__(self):
        self._user_input = None
        self.email = None
        self.first_name = None
        self.last_name = None
        self.email_validated = None
        self.first_name_validated = None
        self.last_name_validated = None
        self.all_fields_validated = None

    @property
    def user_input(self):
        return self._user_input

    @user_input.setter
    def user_input(self, user_input_val):
        self._user_input = user_input_val

    @staticmethod
    def match_regex(template: Pattern[str], given_str: str) -> bool | tuple[str, tuple[int, int]]:
        match = re.search(template, given_str)
        if match:
            return match.group(), match.span()
        return False

    def _validate_names(self, name_str: str):
        first_name_check = InputParser.match_regex(InputParser.FIRST_NAME_REGEX, name_str)
        last_name_check = InputParser.match_regex(InputParser.LAST_NAME_REGEX, name_str)
        if not first_name_check and last_name_check:
            self.first_name_validated = False
        elif first_name_check and not last_name_check:
            self.last_name_validated = False
        elif first_name_check and last_name_check:
            self.first_name, self.last_name = [i.strip() for i in name_str.split(maxsplit=1)]
            self.first_name_validated = True
            self.last_name_validated = True
        else:
            self.first_name_validated = False
            self.last_name_validated = False

    def process(self):
        if self._user_input:
            regex_return = InputParser.match_regex(InputParser.EMAIL_REGEX, self._user_input)
            if regex_return:
                self.email_validated = True
                email, span_indices = regex_return
                self.email = email.strip()
                names = self._user_input[:span_indices[0] + 1]
                self._validate_names(name_str=names)
            else:
                self.email_validated = False
        else:
            raise ValueError("User input string needs to be set first")

    def evaluate_fields(self):
        fields: tuple = (self.first_name_validated,
                         self.last_name_validated,
                         self.email_validated)
        match fields:
            # wrong email
            case (None, None, False):
                print("Incorrect email.")
                return False

            # wrong first name
            case (False, True | None, True):
                print("Incorrect first name.")
                return False

            # wrong last name
            case (True | None, False, True):
                print("Incorrect last name.")
                return False

            # all invalid creds
            case (False, False, False):
                return

            # all valid
            case (True, True, True):
                self.all_fields_validated = True
                return True

            # no match - invalid
            case _:
                return

    def get_data(self) -> dict:
        if self.all_fields_validated:
            return {
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email
            }
        raise ValueError("Some field(s) are not validated")


if __name__ == '__main__':
    x = Student("panda", "dodo", "chaku@gmail.com")
    y = Student("chu", "champ", "alpha@gmail.com")
    z = Student("dragon", "lulu", "psider@gmail.com")
    x.save_student()
    y.save_student()
    z.save_student()
    print(Student.total_students())
    pprint(STUDENT_DATA, indent=2)
