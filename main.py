import argparse
import logging
from common import config
import news_page_objects as news

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _news_scraper(site_id):
    host = config()['news_sites'][site_id]['url']

    logging.info('Beggining scraper for {}'.format(host))
    homepage = news.HomePage(site_id, host)

    for link in homepage.article_links:
        print(link)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    choices = list(config()['news_sites'].keys())
    parser.add_argument(
        "news_site", help="The news site you want to scrape", type=str, choices=choices)

    args = parser.parse_args()
    _news_scraper(args.news_site)
