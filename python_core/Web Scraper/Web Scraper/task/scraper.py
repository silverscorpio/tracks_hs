import requests


def main():
    url = input("Input the URL:\n")
    response = requests.get(url)
    if response.status_code == 200:
        if "content" in response.json():
            print(response.json()["content"])
        else:
            print("Invalid quote resource!")
    else:
        print("Invalid quote resource!")


if __name__ == '__main__':
    main()
