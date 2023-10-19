import requests
from bs4 import BeautifulSoup


def invalid_msg():
    print("Invalid page!")


def main():
    url = input("Input the URL:\n")
    url_keywords = ['articles', 'nature']
    if not all([i in url for i in url_keywords]):
        invalid_msg()
    else:
        url_headers = {'Accept-Language': 'en-US,en;q=0.5'}
        r = requests.get(url, headers=url_headers)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            article_heading = soup.find('title').text
            article_summary = soup.find('meta', {'name': 'description'}).get("content")
            print({
                "title": article_heading,
                "description": article_summary
            })
        else:
            invalid_msg()


if __name__ == '__main__':
    main()
