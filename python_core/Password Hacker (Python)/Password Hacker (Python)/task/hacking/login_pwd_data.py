import string
import json
from random import choice
import itertools

LOWERCASE_ALPHA = string.ascii_lowercase
UPPERCASE_ALPHA = string.ascii_uppercase
NUM_DIGITS = "0123456789"
ELEMENTS_STR = LOWERCASE_ALPHA + NUM_DIGITS
ALL_ELEMENTS_STR = LOWERCASE_ALPHA + UPPERCASE_ALPHA + NUM_DIGITS


def get_pwd_iterator(iterator, n):
    # repeat was the key!!!
    return itertools.product(iterator, repeat=n)


def verify_creds_crack(msg: str) -> bool:
    match json.loads(msg)["result"]:
        case "Wrong password!":
            return True
        case "Exception happened during login":
            return True
        case "Connection success!":
            return True
        case _:
            return False


def gen_case_combos_for_word(word: str) -> list:
    combos = []
    alpha_word_len = len([i for i in word if i.isalpha()])
    alpha_combo = list(zip(word.lower(), word.upper()))
    while len(combos) != 2 ** alpha_word_len:
        chosen_word = ''.join([choice(i) for i in alpha_combo])
        if chosen_word not in combos:
            combos.append(chosen_word)
    return combos


def get_user_login_data(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        pwd_data = f.readlines()
    pwd_data = [i.strip("\n") for i in pwd_data]
    return pwd_data


if __name__ == '__main__':
    print(gen_case_combos_for_word("12345"))
    # print(list(get_pwd_iterator(ELEMENTS_LIST, 2)))
    # check
    # all_elements = get_elements_list()
    # for i in range(2, 3):
    #     pwd_iter = get_pwd_iterator(iterator=all_elements, n=i)
    #     for j in pwd_iter:
    #         print("".join(j))
    #         if "".join(j) == "a9":
    #             print("found")
    #             break
