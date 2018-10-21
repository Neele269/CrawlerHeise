import csv
import crawler

URL = "https://www.heise.de/tp/energie-und-klima/?seite=1"


def write_to_csv(articles):
    with open('articlesHeise.csv', 'w', newline='') as csv_file:
        article_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for article in articles:
            article_writer.writerow(article)


def main():
    write_to_csv(crawler.fetch_articles(URL))


if __name__ == '__main__':
    main()