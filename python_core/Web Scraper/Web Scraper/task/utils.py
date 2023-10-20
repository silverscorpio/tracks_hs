import string
import os
import requests
from bs4 import BeautifulSoup
import bs4

URL_BASE = 'https://www.nature.com'
URL = os.path.join(URL_BASE, 'nature/articles?sort=PubDate&year=2020&page=3')


def clean_article_name(name: str) -> str:
    name = name.strip(" ")
    for i in string.punctuation.join([" ", '—']):
        name = name.replace(i, "_")
    return name


def get_article_title(article: bs4.Tag) -> str:
    title = article.find("a", {"data-track-action": "view article"}).text
    return clean_article_name(title)


def get_article_url(article: bs4.Tag):
    link_path = article.find("a", {"data-track-action": "view article"}).get("href").lstrip("/")
    return os.path.join(URL_BASE, link_path)


def get_article_contents(article_path: str) -> str:
    article_r = requests.get(article_path)
    article_soup = BeautifulSoup(article_r.content, 'html.parser')
    return article_soup.find("p", {"class": "article__teaser"}).text


def save_file(data_to_store: str,
              filename: str) -> None:
    # filename = os.path.join(os.getcwd(), "stuff", filename)
    with open(filename, 'wb') as f:
        f.write(data_to_store.encode())
    print("Content saved.")
