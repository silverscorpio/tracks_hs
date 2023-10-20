from collections import defaultdict
import requests

from bs4 import BeautifulSoup

from utils import (get_article_title,
                   get_article_url,
                   get_article_contents,
                   save_file,
                   URL
                   )


def main():
    articles_info = defaultdict(list)
    r = requests.get(URL)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        articles = soup.find_all("article")
        for article in articles:
            if article.find("span", {"class": "c-meta__type"}).text == "News":
                # title
                title_article = get_article_title(article)
                articles_info["title"].append(title_article)

                # link
                url_article = get_article_url(article)
                articles_info["link"].append(url_article)

                # contents
                contents_article = get_article_contents(url_article)
                articles_info["content"].append(contents_article)

                # save to text file
                save_file(data_to_store=contents_article, filename=title_article + ".txt")
    else:
        print(f"The URL returned {r.status_code}")


if __name__ == '__main__':
    main()
