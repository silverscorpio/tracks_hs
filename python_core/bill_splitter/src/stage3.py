import random


def ans_yes(friends_info: dict) -> str:
    chosen_one = random.choice(list(friends_info.keys()))
    print(f"{chosen_one} is the lucky one!")
    return chosen_one


def lucky_friend(friends: dict) -> str | None:
    print('Do you want to use the "Who is lucky?" feature? Write Yes/No:')
    ans = input()
    if ans == "Yes":
        return ans_yes(friends_info=friends)
    else:
        print("No one is going to be lucky")
