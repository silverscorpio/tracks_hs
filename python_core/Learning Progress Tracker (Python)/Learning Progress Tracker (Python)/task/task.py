def main():
    print("Learning Progress Tracker")
    while True:
        user_input = input().strip()
        if user_input == "exit":
            print("Bye!")
            break
        elif not user_input:
            print("No input")
        else:
            print("Unknown command!")


if __name__ == '__main__':
    main()
