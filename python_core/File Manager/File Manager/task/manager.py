import os

# run the user's program in our generated folders
os.chdir('module/root_folder')


def main():
    print('Input the command')
    user_cmd = input()
    while user_cmd != "quit":
        match user_cmd:
            case "pwd":
                print(os.getcwd())
            case "cd":
                pass
            case "cd ..":
                pass
            case _:
                print("Invalid command")
        user_cmd = input()


if __name__ == '__main__':
    main()
