import random
from stage4 import re_bill_split


def ans_yes(friends_info: dict) -> str:
    chosen_one = random.choice(list(friends_info.keys()))
    print(f"{chosen_one} is the lucky one!")
    return chosen_one


def lucky_friend(friends: dict) -> None:
    print('Do you want to use the "Who is lucky?" feature? Write Yes/No:')
    ans = input()
    if ans == "Yes":
        print(re_bill_split(friends_info=friends, lucky_friend=ans_yes(friends_info=friends)))
    else:
        print("No one is going to be lucky")
        print(friends)
