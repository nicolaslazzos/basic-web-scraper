import argparse
import logging
import pandas as pd
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(filename):
    logger.info('Starting the cleaning process')

    df = _read_data(filename)

    site_id = _extract_site_id(filename)
    df = _add_column(df, 'site_id', site_id)
    df = _extract_host(df)
    df = _fill_missing_titles(df)

    return df


def _read_data(filename):
    logger.info('Reading file {}'.format(filename))
    return pd.read_csv(filename)


def _extract_site_id(filename):
    logger.info('Extracting site id')
    site_id = filename.split('-')[0]
    logger.info('Site id {}'.format(site_id))
    return site_id


def _add_column(df, name, value):
    logger.info('Adding column {}, with value {}'.format(name, value))
    df[name] = value
    return df


def _extract_host(df):
    logger.info('Extracting urls host')
    df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)
    return df

def _fill_missing_titles(df):
    logger.info('Filling missing titles')
    missing_titles_mask = df['title'].isna()
    missing_titles = df[missing_titles_mask]['url'].str.extract(r'(?P<missing_titles>[^/]+)$').applymap(lambda title: title.replace('-', ' '))
    df.loc[missing_titles_mask, 'title'] = missing_titles.loc[:, 'missing_titles']
    return df

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="The path to the raw data", type=str)

    args = parser.parse_args()

    df = main(args.filename)

    print(df['title'])
