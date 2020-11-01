from common import config
import requests
import bs4


class NewsPage:
    def __init__(self, site_id, url):
        self._config = config()['news_sites'][site_id]
        self._queries = self._config['queries']
        self._html = None
        self._url = url

        self._visit(url)

    def _select(self, query_string):
        return self._html.select(query_string)

    def _visit(self, url):
        response = requests.get(url)

        # shows an error if page doestn load
        response.raise_for_status()

        self._html = bs4.BeautifulSoup(response.text, 'html.parser')


class HomePage(NewsPage):
    def __init__(self, site_id, url):
        super().__init__(site_id, url)

    @property
    def article_links(self):
        link_list = []
        for link in self._select(self._queries['homepage_article_links']):
            if link and link.has_attr('href'):
                link_list.append(link)

        return set(link['href'] for link in link_list)


class ArticlePage(NewsPage):
    def __init__(self, site_id, url):
        super().__init__(site_id, url)

    @property
    def body(self):
        result = self._select(self._queries['article_body'])
        body = ''

        for p in result:
            body += p.text

        return body

    @property
    def title(self):
        result = self._select(self._queries['article_title'])
        return result[0].text if len(result) else ''

    @property
    def subtitle(self):
        result = self._select(self._queries['article_subtitle'])
        return result[0].text if len(result) else ''

    @property
    def url(self):
        return self._url
