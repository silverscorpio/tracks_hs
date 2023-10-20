from collections import defaultdict
import requests

from bs4 import BeautifulSoup

from utils import (get_article_title,
                   get_article_url,
                   get_article_contents,
                   save_file,
                   URL_ARTICLES,
                   get_user_inputs,
                   get_query_params,
                   )


def main():
    articles_info = defaultdict(list)
    page_to_search, type_article = get_user_inputs()
    for p in range(1, page_to_search + 1):
        q_params = get_query_params(page_no=p)
        r = requests.get(URL_ARTICLES, params=q_params)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            articles = soup.find_all("article")
            for article in articles:
                if article.find("span", {"class": "c-meta__type"}).text == type_article:
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
                    save_file(data_to_store=contents_article,
                              page_num=p,
                              filename=title_article + ".txt")

        else:
            print(f"The URL returned {r.status_code}")


if __name__ == '__main__':
    main()
