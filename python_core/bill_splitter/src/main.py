from stage1 import get_friends_data
from stage2 import get_bill_and_update_data

if __name__ == '__main__':
    data = get_friends_data()
    if isinstance(data, dict):
        print(get_bill_and_update_data(friends=data))
    elif isinstance(data, str):
        print(data)
