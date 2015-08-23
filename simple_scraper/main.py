import logging
import const
import datetime
import functools
import requests
import bs4


def configure_logger(log=logging.getLogger('dw')):
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(const.CONSOLE_LOGLEVEL)
    console_handler.setFormatter(formatter)
    log.addHandler(console_handler)


def debug_decorator(func):
    @functools.wraps(func)
    def with_logging(*args, **kwargs):
        logger.debug("Starting %r", func.__name__)
        ret = func(*args, **kwargs)
        logger.debug("Finished %r", func.__name__)
        return ret

    return with_logging


@debug_decorator
def extract_links(content):
    soup = bs4.BeautifulSoup(content, 'html.parser')
    logger.debug(soup.title)
    for link in soup.find_all('a'):
        logger.debug(link.get('href'))


@debug_decorator
def get_page(url):
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        logger.debug("GET %r successful", url)
        return r.content
    else:
        r.raise_for_status()


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    logger = logging.getLogger(const.LOGGER_NAME)
    configure_logger(logger)
    logger.info('Script has started')
    res = get_page("http://dsp.org.pl")
    extract_links(res)
    logger.info('Script has finished running. Time elapsed: %s', datetime.datetime.now() - start_time)
    logger.info('-' * 80)
