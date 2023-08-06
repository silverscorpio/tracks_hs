def get_friends_data() -> dict | str:
    print("Enter the number of friends joining (including you):")
    num_friends = int(input())
    if num_friends == 0 or num_friends < 0:
        return "No one is joining for the party"
    counter = 0
    friends_data = {}
    print("Enter the name of every friend (including you), each on a new line:")
    while counter < num_friends:
        friends_data[input()] = 0
        counter += 1
    return friends_data


if __name__ == '__main__':
    print(get_friends_data())
