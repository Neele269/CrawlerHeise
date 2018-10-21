from collections import namedtuple
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

CrawledArticle = namedtuple("CrawledArticle", "title, content, image, author, data, count_comments")


def get_text(post, selector, default):
    element = post.select_one(selector)
    return default if element is None else element.text


def parse_article(url, post):
    title = get_text(post, ".tp_title", "Kein Title vorhanden!")
    content = get_text(post, "p", "Kein Content vorhanden!")
    author = get_text(post, "li.has-author", "Kein Autor vorhanden!")
    data = get_text(post, "time", "Kein Datum vorhanden!")
    count_comments = get_text(post, "span.count.comment_count", "Keine Anzahl der Kommentare vorhanden!")
    img = post.select_one("img")
    image = urljoin(url, img.attrs["src"]) if img is not None else "Kein Bild vorhanden!"
    return CrawledArticle(title, content, image, author, data, count_comments)


def get_next_url(url, doc):
    url_sub = doc.select_one(".seite_weiter")
    if url_sub is not None:
        return urljoin(url, url_sub.attrs["href"])
    return None


def fetch_articles(url):
    articles = []
    while url:
        print(url)
        r = requests.get(url)
        doc = BeautifulSoup(r.text, "html.parser")
        for post in doc.select("article.news.row"):
            articles.append(parse_article(url, post))
            continue
        # url = get_next_url(url, doc)
        url = None
    return articles
