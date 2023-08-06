from stage1 import get_friends_data
from stage2 import get_bill_and_update_data
from stage3 import lucky_friend

if __name__ == '__main__':
    data = get_friends_data()
    if isinstance(data, dict):
        bill_split_data = get_bill_and_update_data(friends=data)
        lucky_friend(friends=bill_split_data)
    elif isinstance(data, str):
        print(data)
