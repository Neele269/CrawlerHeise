import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from .CrawledArticle import CrawledArticle


class ArticleFetcher:
    def __init__(self, url):
        self.url = url
        self.articles = []

    def next_page(self, url):
        self.url = url
        r = requests.get(self.url)
        doc = BeautifulSoup(r.text, "html.parser")
        if doc.select_one(".seite_weiter") is not None:
            print(doc.select_one(".seite_weiter"))
            url_sub = doc.select_one(".seite_weiter").attrs["href"]
            self.url = urljoin(url, url_sub)
            print(url_sub)
            return True
        else:
            print("False")
            return False

    def fetch(self):

        try:

            self.articles = []
            # i = 0

            while True:
                time.sleep(1)
                print(self.url)
                r = requests.get(self.url)
                posts = BeautifulSoup(r.text, "html.parser")

                for post in posts.select("article.news.row"):

                    if post.select_one(".tp_title") is not None:
                        title = post.select_one(".tp_title").text
                    else:
                        title = "Kein Title vorhanden!"
                    print(title)

                    if post.select_one("p") is not None:
                        content = post.select_one("p").text
                    else:
                        content = "Kein Content vorhanden!"
                    print(content)

                    if post.select_one("img") is not None:
                        sub_url = post.select_one("img").attrs["src"]
                        image = urljoin(self.url, sub_url)
                    else:
                        image = "Kein Bild vorhanden!"
                    print(image)

                    if post.select_one("li.has-author") is not None:
                        author = post.select_one("li.has-author").text
                    else:
                        author = "Kein Autor vorhanden!"
                    print(author)

                    if post.select_one("time") is not None:
                        data = post.select_one("time").text
                    else:
                        data = "Kein Datum vorhanden!"
                    print(data)

                    if post.select_one("span.count.comment_count") is not None:
                        count_comments = post.select_one("span.count.comment_count").text
                    else:
                        count_comments = "Keine Anzahl der Kommentare vorhanden!"
                    print(count_comments)

                    crawled = CrawledArticle(title, content, image, author, data, count_comments)
                    self.articles.append(crawled)

                    print("\n\n\n")
                    # i += 1

                    # print(i)

                if not self.next_page(self.url):  # or i >= 42*3:
                    break

            return self.articles

        except:

            print('Die URL ist falsch!')
            print(self.url)
            quit()