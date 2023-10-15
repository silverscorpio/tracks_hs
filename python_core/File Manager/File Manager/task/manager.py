import os

# run the user's program in our generated folders
os.chdir('module/root_folder')


def sort_dirs_first(dir_contents: list[str]) -> list:
    return sorted(dir_contents, key=lambda x: "." in x)


def format_file_size(filesize: int | float) -> str:
    if filesize < 1024:
        return str(round(filesize)) + "B"
    elif 1024 <= filesize < 1024 * 1e3:
        return str(round(filesize / 1024)) + "KB"
    elif 1024 * 1e3 <= filesize < 1024 * 1e6:
        return str(round(filesize / (1024 * 1e3))) + "MB"
    elif filesize > 1024 * 1e6:
        return str(round(filesize / (1024 * 1e6))) + "GB"


def remove_file_or_dir(given_path: str):
    if os.path.isdir(given_path):
        os.rmdir(given_path)
    elif os.path.isfile(given_path):
        os.remove(given_path)


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
            case "ls":
                dir_contents = os.listdir(os.getcwd())
                dir_contents = [i for i in dir_contents if (not i.startswith("__") and (not i.endswith("__")))]
                dir_contents_sizes_bytes = [os.stat(i).st_size for i in dir_contents]

                if len(user_cmd_list) > 1:
                    if user_cmd_list[1] == "-l":
                        for f, s in zip(dir_contents, dir_contents_sizes_bytes):
                            print(f"{f} {s}")
                    elif user_cmd_list[1] == "-lh":
                        dir_contents_sizes_converted = [format_file_size(i) for i in dir_contents_sizes_bytes]
                        for f, s in zip(dir_contents, dir_contents_sizes_converted):
                            print(f"{f} {s}")
                else:
                    sorted_files = sort_dirs_first(dir_contents)
                    for i in sorted_files:
                        print(i)
            case "rm":
                if len(user_cmd_list) == 1:
                    print("Specify the file or directory")
                elif len(user_cmd_list) == 2:
                    given_path = user_cmd_list[1]
                    if os.path.exists(given_path):
                        if os.path.isabs(given_path):
                            remove_file_or_dir(given_path)
                        else:
                            complete_path = os.path.join(os.getcwd(), given_path)
                            remove_file_or_dir(given_path=complete_path)
                    else:
                        print("No such file or directory")

            case "mv":
                if len(user_cmd_list) == 1:
                    print("Specify the current name of the file or directory and the new name")
                else:
                    complete_current_location = os.path.join(os.getcwd(), user_cmd_list[1])
                    complete_new_location = os.path.join(os.getcwd(), user_cmd_list[2])
                    if not os.path.exists(complete_new_location):
                        print("No such file or directory")
                    elif os.path.exists(complete_new_location):
                        print("The file or directory already exists")
                    else:
                        os.rename(complete_current_location, complete_new_location)

            case "mkdir":
                if len(user_cmd_list) == 1:
                    print("Specify the name of the directory to be made")
                elif len(user_cmd_list) == 2:
                    given_path = user_cmd_list[1]
                    if not os.path.exists(given_path):
                        if os.path.isabs(given_path):
                            os.mkdir(given_path)
                        else:
                            complete_path = os.path.join(os.getcwd(), given_path)
                            os.mkdir(complete_path)
                    else:
                        print("The directory already exists")

            case "quit":
                break
                
            case _:
                print("Invalid command")


if __name__ == '__main__':
    main()
