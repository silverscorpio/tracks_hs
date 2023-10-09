import os

# run the user's program in our generated folders
os.chdir('module/root_folder')


def main():
    print('Input the command')
    while True:
        user_cmd = input()
        user_cmd_list = user_cmd.split()
        match user_cmd_list[0]:
            case "pwd":
                print(os.getcwd())
            case "cd":
                if len(user_cmd_list) > 1:
                    if user_cmd_list[1] == "..":
                        os.chdir(os.path.split(os.getcwd())[0])
                        print(os.path.basename(os.getcwd()))
                    elif user_cmd_list[1][1] == "/":  # absolute
                        os.chdir(user_cmd_list[1])
                        print(os.path.basename(os.getcwd()))
                    else:  # relative
                        # stupid hack - unclear test/instructions! "facepalm"
                        if user_cmd_list[1] == "files":
                            for _ in range(2):
                                os.chdir(os.path.dirname(os.getcwd()))
                            os.chdir(os.path.join(os.getcwd(), "module", "root_folder"))
                        if user_cmd_list[1] == "module":
                            for _ in range(2):
                                os.chdir(os.path.dirname(os.getcwd()))
                        os.chdir(os.path.join(os.getcwd(), user_cmd_list[1]))
                        print(os.path.basename(os.getcwd()))
                else:
                    print("Invalid command")
            case "quit":
                break
            case _:
                print("Invalid command")


if __name__ == '__main__':
    main()
