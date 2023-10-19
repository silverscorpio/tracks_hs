import requests


def save_binary_file(data_to_store: bytes, file_name: str = 'source.html') -> None:
    with open(file_name, 'wb') as f:
        f.write(data_to_store)
    print("Content saved.")


def main():
    url = input("Input the URL:\n")
    r = requests.get(url)
    if r.status_code == 200:
        content = r.content
        save_binary_file(data_to_store=content)
    else:
        print(f"The URL returned {r.status_code}")


if __name__ == '__main__':
    main()
