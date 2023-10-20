import string
import os
from collections import defaultdict

import bs4
import requests
from bs4 import BeautifulSoup

URL_BASE = 'https://www.nature.com'
URL = os.path.join(URL_BASE, 'nature/articles?sort=PubDate&year=2020&page=3')


def clean_article_name(name: str) -> str:
    name = name.strip(" ")
    for i in string.punctuation.join([" ", '—']):
        name = name.replace(i, "_")
    return name


def get_article_title(article: bs4.Tag) -> str:
    # article.find("a", {"data-track-action": "view article"}).text
    # 'The lightning-fast quest for COVID vaccines — and what it means for other diseases'
    title = article.find("a", {"data-track-action": "view article"}).text
    return clean_article_name(title)


def get_article_url(article: bs4.Tag):
    link_path = article.find("a", {"data-track-action": "view article"}).get("href").lstrip("/")
    return os.path.join(URL_BASE, link_path)


def get_article_contents(article_path: str) -> str:
    article_r = requests.get(article_path)
    article_soup = BeautifulSoup(article_r.content, 'html.parser')
    return article_soup.find("p", {"class": "article__teaser"}).text


def save_file(data_to_store,
              filename: str) -> None:
    complete_filename = os.path.join(os.getcwd(), "stuff", filename)
    with open(complete_filename, 'wb') as f:
        f.write(data_to_store)
    print("Content saved.")


def main():
    articles_info = defaultdict(list)
    r = requests.get(URL)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        articles = soup.find_all("article")
        for article in articles:
            if "News" in article.find("span", {"class": "c-meta__type"}).text:
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
