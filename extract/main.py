import argparse
import logging
import re
from datetime import datetime
import csv
import io
from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

from common import config
import news_page_objects as news

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

is_well_formed_link = re.compile(r'^https?://.+/.+$')
is_root_path = re.compile(r'^/.+$')


def _news_scraper(site_id):
    host = config()['news_sites'][site_id]['url']

    logging.info('Beggining scraper for {}'.format(host))
    homepage = news.HomePage(site_id, host)

    articles = []

    for link in homepage.article_links:
        article = _fetch_article(site_id, host, link)

        if article:
            logger.info('Article fetched')
            articles.append(article)
            print(article.title)

    print(len(articles))

    _save_articles(site_id, articles)


def _save_articles(site_id, articles):
    now = datetime.now().strftime('%Y_%m_%d')
    file_name = '{}-{}-articles.csv'.format(site_id, now)

    # filtering @properties to get headers because python recognize them as functions by default
    csv_headers = list(
        filter(lambda prop: not prop.startswith('_'), dir(articles[0])))

    with io.open(file_name, 'w+', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)

        for article in articles:
            row = [str(getattr(article, prop)) for prop in csv_headers]
            writer.writerow(row)


def _fetch_article(site_id, host, link):
    link = _build_link(host, link)

    logging.info('Started fetching article at {}'.format(link))

    article = None

    try:
        article = news.ArticlePage(site_id, link)
    except (HTTPError, MaxRetryError) as e:
        logger.warning('Error while fetching the article', exc_info=False)

    if article and not article.body:
        logger.warning('Invalid article, there is no body')
        return None

    return article


def _build_link(host, link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return '{}{}'.format(host, link)
    else:
        return '{host}/{uri}'.format(host=host, uri=link)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    choices = list(config()['news_sites'].keys())
    parser.add_argument(
        "news_site", help="The news site you want to scrape", type=str, choices=choices)

    args = parser.parse_args()
    _news_scraper(args.news_site)
