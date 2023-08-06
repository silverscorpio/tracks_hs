def get_bill_and_update_data(friends: dict) -> dict:
    print("Enter the total bill value:")
    bill = float(input())
    bill_per_person = round(bill / len(friends), 2)
    for k in friends:
        friends[k] = bill_per_person
    return friends
