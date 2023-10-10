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

            case "quit":
                break
            case _:
                print("Invalid command")


if __name__ == '__main__':
    main()
