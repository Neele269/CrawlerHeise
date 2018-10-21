import csv
import crawler


url = "https://www.heise.de/tp/energie-und-klima/?seite=1"


def main():
    fetcher = crawler.ArticleFetcher(url)
    write_to_csv(fetcher.fetch())


def write_to_csv(articles):
    with open('articlesHeisse.csv', 'w', newline='') as csv_file:
        article_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for article in articles:
            article_writer.writerow([article.title, article.content, article.image, article.author, article.data,
                                     article.count_comments])


if __name__ == '__main__':
    main()
