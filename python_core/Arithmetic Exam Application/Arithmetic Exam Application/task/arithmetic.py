import random


def get_random_operation() -> str:
    return random.choice(["+", "-", "*"])


def get_random_num() -> int:
    return random.randint(2, 9)


def generate_question() -> str:
    return f"{get_random_num()} {get_random_operation()} {get_random_num()}"


def get_question_ans(question: str) -> int:
    question_data: list = question.split()
    num1, operation, num2 = int(question_data[0]), question_data[1], int(question_data[2])

    match operation:
        case '+':
            return num1 + num2
        case "-":
            return num1 - num2
        case "*":
            return num1 * num2


def main():
    given_question = generate_question()
    print(given_question)
    user_ans = int(input())
    if user_ans == get_question_ans(question=given_question):
        print("Right!")
    else:
        print("Wrong!")


if __name__ == '__main__':
    main()
