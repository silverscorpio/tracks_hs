import random

LEVEL_OPTIONS = {
    "1": "simple operations with numbers 2-9",
    "2": "integral squares of 11-29"
}


def save_results_to_file(data: dict):
    with open("results.txt", "a") as f:
        f.write(
            f"{data["name"]}: {data["score"]}/5 in level {data["option"]} {LEVEL_OPTIONS[data["option"]]}.")

    print("The results are saved in 'results.txt'")


def get_random_operation() -> str:
    return random.choice(["+", "-", "*"])


def get_random_num() -> int:
    return random.randint(2, 9)


def get_num_integral_squares():
    return random.randint(11, 29)


def generate_question(option: int) -> str:
    if option == 1:
        return f"{get_random_num()} {get_random_operation()} {get_random_num()}"
    elif option == 2:
        return f"{get_num_integral_squares()}"


def get_question_ans(question: str, option: int) -> int:
    if option == 1:
        question_data: list = question.split()
        num1, operation, num2 = int(question_data[0]), question_data[1], int(question_data[2])
        match operation:
            case '+':
                return num1 + num2
            case "-":
                return num1 - num2
            case "*":
                return num1 * num2
    elif option == 2:
        return int(question) ** 2


def validate_user_ans(ans: str) -> bool:
    try:
        _ = int(ans)
    except ValueError:
        print("Incorrect format.")
        return False
    else:
        return True


def get_starting_option() -> str:
    return input(f"""
Which level do you want? Enter a number:
1 - {LEVEL_OPTIONS["1"]},
2 - {LEVEL_OPTIONS["2"]}
""")


def main():
    score, question_count = 0, 0

    while True:
        user_choice = get_starting_option()
        ans_validate = validate_user_ans(ans=user_choice)
        if ans_validate:
            break

    user_choice = int(user_choice)
    while question_count != 5:
        given_question = generate_question(option=user_choice)
        print(given_question)
        question_count += 1

        while True:
            user_ans = input()
            ans_validate = validate_user_ans(ans=user_ans)
            if ans_validate:
                break
        user_ans = int(user_ans)
        if user_ans == get_question_ans(question=given_question, option=user_choice):
            print("Right!")
            score += 1
        else:
            print("Wrong!")

    save_results = input(f"Your mark is {score}/5. Would you like to save the result? Enter yes or no.\n")
    if save_results in ("yes", "YES", "y", "Yes"):
        user_name = input("What is your name?\n")
        user_data = {
            "name": user_name,
            "option": str(user_choice),
            "score": score
        }
        save_results_to_file(data=user_data)


if __name__ == '__main__':
    main()
