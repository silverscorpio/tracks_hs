# write your code here

def main() -> int:
    user_input_list = input().split()
    num1, operation, num2 = int(user_input_list[0]), user_input_list[1], int(user_input_list[2])

    match operation:
        case '+':
            return num1 + num2
        case "-":
            return num1 - num2
        case "*":
            return num1 * num2


if __name__ == '__main__':
    print(main())
