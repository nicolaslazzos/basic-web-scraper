import argparse
import logging
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sites_ids = ['el_universal', 'el_pais']


def main():
    _extract()
    _transform()
    _load()


def _extract():
    logger.info('Starting extract process')

    cwd = '.\\extract'

    print(cwd)

    for site_id in sites_ids:
        subprocess.run(['python', 'main.py', site_id], cwd=cwd, shell=True)
        subprocess.run(['move', '{}*.csv'.format(site_id),
                        '..\\transform\\{}.csv'.format(site_id)], cwd=cwd, shell=True)


def _transform():
    logger.info('Starting transform process')

    cwd = '.\\transform'

    for site_id in sites_ids:
        subprocess.run(
            ['python', 'main.py', '{}.csv'.format(site_id)], cwd=cwd, shell=True)
        subprocess.run(['move', 'clean-{}.csv'.format(site_id),
                        '..\\load\\'.format()], cwd=cwd, shell=True)
        subprocess.run(['del', '{}.csv'.format(site_id)], cwd=cwd, shell=True)


def _load():
    logger.info('Starting load process')

    cwd = '.\\load'

    for site_id in sites_ids:
        subprocess.run(
            ['python', 'main.py', 'clean-{}.csv'.format(site_id)], cwd=cwd, shell=True)


if __name__ == '__main__':
    main()
