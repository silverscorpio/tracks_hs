import string
import itertools

LOWERCASE_ALPHA = string.ascii_lowercase
NUM_DIGITS = "0123456789"


def get_elements_list() -> list:
    elements = []
    elements.extend(list(LOWERCASE_ALPHA))
    elements.extend(list(NUM_DIGITS))
    return elements


def get_pwd_iterator(iterator, n):
    # repeat was the key!!!
    return itertools.product(iterator, repeat=n)


if __name__ == '__main__':
    # check
    all_elements = get_elements_list()
    for i in range(2, 3):
        pwd_iter = get_pwd_iterator(iterator=all_elements, n=i)
        for j in pwd_iter:
            print("".join(j))
            if "".join(j) == "a9":
                print("found")
                break
