def re_bill_split(friends_info: dict, lucky_friend: str) -> dict:
    orig_bill = sum(list(friends_info.values()))
    friends_info[lucky_friend] = 0
    for k in friends_info:
        if k != lucky_friend:
            friends_info[k] = round(orig_bill / (len(friends_info) - 1), 2)
    return friends_info
