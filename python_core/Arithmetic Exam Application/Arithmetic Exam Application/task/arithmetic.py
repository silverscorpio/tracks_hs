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


def validate_user_ans(ans: str) -> bool:
    try:
        _ = int(ans)
    except ValueError:
        print("Incorrect format.")
        return False
    else:
        return True


def main():
    score = 0
    question_count = 0
    while question_count != 5:
        given_question = generate_question()
        print(given_question)
        question_count += 1
        while True:
            user_ans = input()  # value error
            ans_validate = validate_user_ans(ans=user_ans)
            if ans_validate:
                break
        user_ans = int(user_ans)
        if user_ans == get_question_ans(question=given_question):
            print("Right!")
            score += 1
        else:
            print("Wrong!")

    print(f"Your mark is {score}/5.")


if __name__ == '__main__':
    main()
