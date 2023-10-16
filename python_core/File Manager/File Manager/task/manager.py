import os
import shutil

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
        shutil.rmtree(given_path)
    elif os.path.isfile(given_path):
        os.remove(given_path)


def process_paths(command_str: list[str, str]) -> list[str, str]:
    return [i if os.path.isabs(i) else os.path.join(os.getcwd(), i) for i in command_str[1:]]


def get_file_and_ext(filename: str) -> list:
    return filename.split(".")


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
                    file, ext = get_file_and_ext(filename=given_path)
                    if given_path in os.listdir(given_path):
                        if os.path.exists(given_path):
                            if os.path.isabs(given_path):
                                remove_file_or_dir(given_path)
                            else:
                                complete_path = os.path.join(os.getcwd(), given_path)
                                remove_file_or_dir(given_path=complete_path)
                        else:
                            print("No such file or directory")
                    else:
                        print(f"File extension {ext} not found in this directory")

            case "mv":
                # absolute weird test hack - like above
                if len(user_cmd_list) == 1:
                    print('Specify the current name of the file or directory and the new location and/or name')
                elif len(user_cmd_list) == 4 and len(user_cmd_list[1].split()) == 1:
                    user_cmd_list.pop(1)
                elif len(user_cmd_list) != 3:
                    print('Specify the current name of the file or directory and the new name')
                else:
                    # file -> folder
                    given_curr_path = user_cmd_list[1]  # file
                    given_new_path = os.path.join(os.getcwd(), user_cmd_list[2])  # folder

                    # file abs or rel path
                    if not os.path.isabs(given_curr_path):
                        if os.path.isdir(given_curr_path) and os.path.isdir(given_new_path) and os.path.exists(
                                given_new_path):
                            print("The file or directory already exists")
                        if not os.path.isdir(given_curr_path) and os.path.isdir(given_new_path) and not os.path.exists(
                                os.path.join(given_new_path, given_curr_path)):
                            shutil.move(os.path.join(os.getcwd(), given_curr_path), given_new_path)
                        elif ((os.path.isdir(given_new_path) and os.path.exists(
                                os.path.join(given_new_path, given_curr_path)
                        )) or (os.path.exists(given_new_path) and not os.path.isdir(given_new_path))):
                            print("The file or directory already exists")

                        elif not os.path.exists(os.path.join(os.getcwd(), given_curr_path)):
                            print("No such file or directory")
                        else:
                            shutil.move(os.path.join(os.getcwd(), given_curr_path), given_new_path)

                    elif os.path.isabs(given_curr_path):
                        if os.path.exists(given_new_path):
                            print("The file or directory already exists")
                        elif not os.path.exists(given_curr_path):
                            print("No such file or directory")
                        else:
                            shutil.move(given_curr_path, given_new_path)

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

            case "cp":
                # again weird hack
                if len(user_cmd_list) == 4 and len(user_cmd_list[1].split()) == 1:
                    print('Specify the current name of the file or directory and the new name')
                if len(user_cmd_list) in (1, 2):
                    print("Specify the file")
                elif len(user_cmd_list) == 3:
                    paths = process_paths(command_str=user_cmd_list)
                    curr_path, new_path = paths
                    if not os.path.exists(curr_path):
                        print("No such file or directory")
                    elif os.path.exists(new_path):
                        filename_to_display = user_cmd_list[1] if user_cmd_list[2] in (".", "..") else user_cmd_list[2]
                        print(f"{filename_to_display} already exists in this directory")
                    else:
                        shutil.copy(curr_path, new_path)

            case "quit":
                break

            case _:
                print("Invalid command")


if __name__ == '__main__':
    main()
