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
    """
    Small decorator to save on writing the same code over and over again. Useful for debugging.
    """

    @functools.wraps(func)
    def with_logging(*args, **kwargs):
        logger.debug("Starting %r", func.__name__)
        ret = func(*args, **kwargs)
        logger.debug("Finished %r", func.__name__)
        return ret

    return with_logging


@debug_decorator
def extract_links(content):
    """
    Extracts links from page using Beautiful Soup.
    :param content: HTML string with webpage content
    :return: list of links
    """
    soup = bs4.BeautifulSoup(content, 'html.parser')
    logger.debug(soup.title)
    for link in soup.find_all('a'):
        yield clean_link(link.get('href'))


@debug_decorator
def get_page(url):
    """
    Gets the HTTP page using requests.
    :param url: URL to be fetched
    :return: Webpage as HTML String
    """
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        logger.debug("GET %r successful", url)
        return r.content
    else:
        r.raise_for_status()


def clean_link(link):
    """
    (Very) Naive function to create absolute links from relative paths.
    :param link: String containing link
    :return: String containing absolute link
    """
    if "http://" in link:
        return link
    else:
        return const.STARTING_PAGE + link


@debug_decorator
def crawl():
    crawled_set = set()  # A set to check whether link has been visited or not
    queue = [const.STARTING_PAGE]  # Queue for links to be crawled. Simple list because app isn't threaded.
    pages_count = 0  # Pages crawled
    while len(queue) > 0:
        pass


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    logger = logging.getLogger(const.LOGGER_NAME)
    configure_logger(logger)
    logger.info('Script has started')
    res = get_page("http://dsp.org.pl")
    for l in extract_links(res):
        logger.debug(l)
    logger.info('Script has finished running. Time elapsed: %s', datetime.datetime.now() - start_time)
    logger.info('-' * 80)
