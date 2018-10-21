import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from collections import namedtuple


class ArticleFetcher:
    def __init__(self, url):
        self.url_parsed = urlparse(url)
        if "seite=1" in self.url_parsed.query:
            self.url = self.url_parsed.scheme + '://' + self.url_parsed.netloc + self.url_parsed.path
        else:
            self.url = url
        self.articles = []

    def next_page(self, url):
        self.url = url
        r = requests.get(self.url)
        doc = BeautifulSoup(r.text, "html.parser")
        if doc.select_one(".seite_weiter") is not None:
            if "seite=" in urlparse(self.url).query:
                url_sub = doc.select_one(".seite_weiter").attrs["href"]
            else:
                url_sub = '?seite=1'
            self.url = urljoin(url, url_sub)
            return True
        else:
            print("False")
            return False

    def fetch(self):
        try:
            self.articles = []
            # i = 0

            while self.next_page(self.url):  # or i >= 42*3:
                time.sleep(1)
                print(self.url)
                r = requests.get(self.url)
                posts = BeautifulSoup(r.text, "html.parser")

                for post in posts.select("article.news.row"):
                    if post.select_one(".tp_title") is not None:
                        title = post.select_one(".tp_title").text
                    else:
                        title = "Kein Title vorhanden!"
                    # print(title)

                    if post.select_one("p") is not None:
                        content = post.select_one("p").text
                    else:
                        content = "Kein Content vorhanden!"
                    # print(content)

                    if post.select_one("img") is not None:
                        sub_url = post.select_one("img").attrs["src"]
                        image = urljoin(self.url, sub_url)
                    else:
                        image = "Kein Bild vorhanden!"
                    # print(image)

                    if post.select_one("li.has-author") is not None:
                        author = post.select_one("li.has-author").text
                    else:
                        author = "Kein Autor vorhanden!"
                    # print(author)

                    if post.select_one("time") is not None:
                        data = post.select_one("time").text
                    else:
                        data = "Kein Datum vorhanden!"
                    # print(data)

                    if post.select_one("span.count.comment_count") is not None:
                        count_comments = post.select_one("span.count.comment_count").text
                    else:
                        count_comments = "Keine Anzahl der Kommentare vorhanden!"
                    # print(count_comments)

                    Article = namedtuple('Article', 'title, content, image, author, data, count_comments')
                    crawled = Article(title, content, image, author, data, count_comments)
                    print(crawled)
                    self.articles.append(crawled)
                    # print("\n\n\n")
                    # i += 1
                    # print(i)
                break
            return self.articles
        except:
            print('Die URL ist falsch!')
            print(self.url)
            exit()
