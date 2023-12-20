import re
from re import Pattern
import uuid
from pprint import pprint
from collections import defaultdict

# student info
STUDENT_DATA: defaultdict = defaultdict(dict)

# regex patterns
FIRST_NAME_REGEX = re.compile(r"^(?![-'])(?:(([A-Za-z])|((['-])(?![-'])))){2,}\b[^-']", flags=re.ASCII)
LAST_NAME_REGEX = re.compile(r" (?![-'])(?:(([A-Za-z])|((['-])(?![-'])))){2,}\b[^'-]$", flags=re.ASCII)
EMAIL_REGEX = re.compile(r" (?:[a-zA-Z0-9_\.])+@(?:[a-zA-Z0-9_]+\.[a-z0-9]{1,3})", flags=re.ASCII)
SCORES_REGEX = re.compile(r"^\d{1,}( \d{1,}){4}$", flags=re.ASCII)
ID_REGEX = re.compile(r"\d{1,}", flags=re.ASCII)


def get_student_data():
    pprint(STUDENT_DATA, indent=4)


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


def get_all_students():
    if STUDENT_DATA:
        print("Students:")
        for id_student in STUDENT_DATA.keys():
            print(id_student)
        return
    print("No students found.")


def check_if_email_exists(email_to_check: str) -> bool:
    return True if email_to_check in [record["email"] for record in STUDENT_DATA.values()] else False


def check_if_id_exists(id_to_check: str) -> bool:
    return True if id_to_check in STUDENT_DATA.keys() else False


def match_regex(template: Pattern[str], given_str: str) -> bool | tuple[str, tuple[int, int]]:
    match = re.search(template, given_str)
    if match:
        return match.group(), match.span()
    return False


def check_id_scores_regex(score_str: str) -> tuple[str, str] | bool:
    regex_match = match_regex(template=SCORES_REGEX, given_str=score_str)
    if regex_match:
        student_id, scores = score_str.split(maxsplit=1)[0], score_str.split(maxsplit=1)[1]
        return student_id, scores
    return False


def store_scores(scores_str: str, student_id: str) -> bool:
    scores_int = [int(i.strip()) for i in scores_str.split()]
    STUDENT_DATA[student_id]["submissions"].append(scores_int)
    for sub, score in zip(STUDENT_DATA[student_id]["scores"].keys(), scores_int):
        STUDENT_DATA[student_id]["scores"][sub] += score
    print("Points updated.")
    return True


def process_id_scores(score_str: str) -> bool:
    raw_student_id = score_str.split()[0]
    try:
        raw_student_id = int(raw_student_id)
    except ValueError:
        print(f"No student is found for id={raw_student_id}")
        return False

    regex_result = check_id_scores_regex(score_str=score_str)
    if not regex_result:
        print("Incorrect points format.")
        return False
    student_id, scores = regex_result
    student_id = student_id.strip()
    if not check_if_id_exists(id_to_check=student_id):
        print(f"No student is found for id={student_id}")
        return False
    store_scores(scores_str=scores, student_id=student_id)


def check_id(given_id: str):
    id_match = match_regex(template=ID_REGEX, given_str=given_id)
    if id_match:
        student_id = id_match[0]
        if not check_if_id_exists(id_to_check=student_id):
            print(f"No student is found for id={student_id}")
            return
        sc1, sc2, sc3, sc4 = STUDENT_DATA[student_id]["scores"].values()
        print(f"{student_id} points: Python={sc1}; DSA={sc2}; Databases={sc3}; Flask={sc4}")
    elif not id_match:
        print(f"No student is found for id={given_id}")
        return


# classes
class Statistic:
    def __init__(self):
        if not STUDENT_DATA:
            print("""
Most popular: n/a
Least popular: n/a
Highest activity: n/a
Lowest activity: n/a
Easiest course: n/a
Hardest course: n/a
""")
        else:
            print(f"""
Most popular: {self.most_popular()}
Least popular: {self.least_popular()}
Highest activity: {self.highest_activity()}
Lowest activity: {self.lowest_activity()}
Easiest course: {self.easiest()}
Hardest course: {self.hardest()}
""")

    def most_popular(self) -> str:
        pass

    def least_popular(self) -> str:
        pass

    def highest_activity(self) -> str:
        pass

    def lowest_activity(self) -> str:
        pass

    def easiest(self) -> str:
        pass

    def hardest(self) -> str:
        pass


class Student:
    student_count: int = 0

    def __new__(cls, first_name, last_name, email):
        cls.student_count += 1
        return super().__new__(cls)

    def __init__(self, first_name, last_name, email):
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.email: str = email
        self.scores: dict = {"py": 0, "dsa": 0, "db": 0, "flask": 0}
        self.submissions: list = []
        self.student_id = str(Student.student_count)

    def save_student(self) -> None:
        # key get uuid from id changed to self student id
        STUDENT_DATA[self.student_id] = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "scores": self.scores,
            "submissions": self.submissions
        }
        print("The student has been added.")

    @staticmethod
    def total_students() -> int:
        return Student.student_count

    def __str__(self):
        # key get uuid from id changed to self student id
        return f"{self.student_id} - {self.first_name} {self.last_name}"


class InputParser:
    """
    extract the email (easier) from the input string and use the match to split and get the name
    """

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

    def _validate_names(self, name_str: str):
        first_name_check = match_regex(FIRST_NAME_REGEX, name_str)
        last_name_check = match_regex(LAST_NAME_REGEX, name_str)
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
            regex_return = match_regex(EMAIL_REGEX, self._user_input)
            if regex_return:
                email, span_indices = regex_return
                # check for existing email
                if not check_if_email_exists(email_to_check=email.strip()):
                    self.email_validated = True
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

            # email already taken
            case (None, None, None):
                print("This email is already taken.")
                return False

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
    x.save_student()
    y = Student("chu", "champ", "alpha@gmail.com")
    y.save_student()
    z = Student("dragon", "lulu", "psider@gmail.com")
    z.save_student()
    STUDENT_DATA['1']['scores'] = {'py': 1, 'dsa': 2, 'db': 3, 'flask': 4}
    STUDENT_DATA['1']['scores'] = {'py': 0, 'dsa': 9, 'db': 10, 'flask': 6}
    STUDENT_DATA['2']['scores'] = {'py': 10, 'dsa': 20, 'db': 30, 'flask': 50}
    STUDENT_DATA['3']['scores'] = {'py': 35, 'dsa': 9, 'db': 78, 'flask': 90}
    pprint(STUDENT_DATA, indent=4)
    # most popular
    enrollments = {"py": 0, "dsa": 0, "db": 0, "flask": 0}
    for k, v in STUDENT_DATA.items():
        for subject in enrollments.keys():
            if v["scores"][subject] > 0:
                enrollments[subject] += 1

    # py_scores = {k: v['scores']["py"] for k, v in STUDENT_DATA.items()}
    print(enrollments)
