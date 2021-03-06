import argparse
import logging
import pandas as pd
import hashlib
from urllib.parse import urlparse
import nltk
from nltk.corpus import stopwords

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

stop_words = set(stopwords.words('spanish'))


def main(filename):
    logger.info('Starting the cleaning process')

    df = _read_data(filename)

    site_id = _extract_site_id(filename)
    df = _add_column(df, 'site_id', site_id)
    df = _extract_host(df)
    df = _fill_missing_titles(df)
    df = _set_rows_uids(df)
    df = _remove_escape_chars(df)
    df = _tokenize_column(df, 'title')
    df = _tokenize_column(df, 'body')
    df = _remove_duplicates(df, 'title')
    df = _remove_duplicates(df, 'url')
    df = _drop_rows_with_missing_data(df)

    _save_data(df, filename)

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
    missing_titles = df[missing_titles_mask]['url'].str.extract(
        r'(?P<missing_titles>[^/]+)$').applymap(lambda title: title.replace('-', ' '))
    df.loc[missing_titles_mask, 'title'] = missing_titles.loc[:, 'missing_titles']
    return df


def _set_rows_uids(df):
    logger.info('Setting rows uids')
    uids = df.apply(lambda row: hashlib.md5(
        bytes(row['url'].encode())).hexdigest(), axis=1)
    df['uid'] = uids
    df.set_index('uid', inplace=True)
    return df


def _remove_escape_chars(df):
    logger.info('Removing escape characters from body')
    stripped_body = df.apply(lambda row: row['body'].replace(
        '\n', '').replace('\r', ''), axis=1)
    df['body'] = stripped_body
    return df


def _tokenize_column(df, column_name):
    logger.info('Tokenizing {} column'.format(column_name))
    tokenized = (df.apply(lambda row: nltk.word_tokenize(row[column_name]), axis=1)
                 .apply(lambda tokens: list(filter(lambda token: token.isalpha(), tokens)))
                 .apply(lambda tokens: list(map(lambda token: token.lower(), tokens)))
                 .apply(lambda words_list: len(list(filter(lambda word: word not in stop_words, words_list)))))

    df['n_tokens_{}'.format(column_name)] = tokenized
    return df


def _remove_duplicates(df, column_name):
    logger.info('Removing duplicate entries from {} column'.format(column_name))
    df.drop_duplicates(subset=[column_name], keep='first', inplace=True)
    return df


def _drop_rows_with_missing_data(df):
    logger.info('Removing rows with missing data')
    return df.dropna()


def _save_data(df, filename):
    clean_filename = 'clean-{}'.format(filename)
    logger.info('Exporting datafram to {}'.format(clean_filename))
    df.to_csv(clean_filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="The path to the raw data", type=str)

    args = parser.parse_args()

    df = main(args.filename)

    print(df)
