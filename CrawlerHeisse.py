import csv
import crawler


url = "https://www.heise.de/tp/energie-und-klima/"
fetcher = crawler.ArticleFetcher(url)
articles = fetcher.fetch()

with open('articlesHeisse.csv', 'w', newline='') as csv_file:
    article_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for article in articles:
        article_writer.writerow([article.title, article.content, article.image, article.author, article.data,
                                 article.count_comments])
