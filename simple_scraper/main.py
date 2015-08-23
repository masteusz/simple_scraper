import logging
import const
import datetime
import functools
import requests
import bs4
import sys


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
    logger = logging.getLogger(const.LOGGER_NAME)  # Needed for unit testing

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
    Generator that extracts links from page using Beautiful Soup.
    :param content: HTML string with webpage content
    :return: list of links
    """
    if content is not None:
        soup = bs4.BeautifulSoup(content, 'html.parser')
        for link in soup.find_all('a'):
            yield clean_link(link.get('href'))


# TODO: Redundant - might be merged with function above
@debug_decorator
def extract_images(content):
    """
    Generator that extracts images from page using Beautiful Soup.
    :param content: HTML string with webpage content
    :return: links to images
    """
    if content is not None:
        soup = bs4.BeautifulSoup(content, 'html.parser')
        for link in soup.find_all('img', src=True):
            yield link.get("src")


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
    if link is None:
        return None
    if "mailto" in link:  # Omit maillinks
        return None
    if "#" in link:  # Omit tag links
        return None

    for ext in const.UNWANTED:
        if ext in link:
            return None

    if "http://" in link or "https://" in link:
        return link
    else:
        if link.startswith("/"):
            return const.STARTING_PAGE + link.lstrip("/")
        return const.STARTING_PAGE + link


@debug_decorator
def crawl():
    """
    Crawling pages in BFS manner.
    :return: Dictionary containing flat pagemap
    """
    crawled_set = set()  # A set to check whether link has been visited or not
    pagemap = {}
    queue = [const.STARTING_PAGE]  # Queue for links to be crawled. Simple list because app isn't threaded.
    while len(queue) > 0:
        current_link = queue[0]
        queue = queue[1:]  # Remove first element from queue

        if current_link in crawled_set:
            logger.debug("Omitting %r", current_link)
            continue

        logger.info("Processing %r", current_link)
        content = None
        try:
            content = get_page(current_link)
        except:  # TODO: Change very broad except clause
            e = sys.exc_info()[0]
            logger.error("Error while retrieving page %r: %r", current_link, e)

        pagemap[current_link] = {"links": set(), "images": set()}

        # Extract links
        for link in extract_links(content):
            if link is None:
                continue

            # Add links to pagemap
            pagemap[current_link]["links"].add(link)

            # If page belongs to current domain then add it to queue
            if const.STARTING_PAGE in link:
                queue.append(link)

        # Extract images
        for link in extract_images(content):
            if link is None:
                continue

            # Add image to pagemap
            pagemap[current_link]["images"].add(link)

        # Add page to processed set
        crawled_set.add(current_link)
        logger.info("Finished processing %r. Links found: %r, images found: %r", current_link,
                    len(pagemap.get(current_link).get("links")),
                    len(pagemap.get(current_link).get("images")),
                    )

    return pagemap


@debug_decorator
def save_to_markdown(pagemap):
    with open(const.MARKDOWN_FILENAME, "w+") as savefile:
        savefile.write("# " + const.STARTING_PAGE + "\n\n")

        for page in sorted(pagemap):
            savefile.write("## " + page + "\n")
            savefile.write("### Links:\n\n")

            for link in sorted(pagemap.get(page).get("links")):
                savefile.write("* " + link.encode('ascii', 'ignore') + "\n")

            savefile.write("\n### Images:\n\n")
            for image in sorted(pagemap.get(page).get("images")):
                savefile.write("* " + image.encode('ascii', 'ignore') + "\n")
            savefile.write("\n")


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    logger = logging.getLogger(const.LOGGER_NAME)
    configure_logger(logger)
    logger.info('Script has started')

    pgmap = crawl()
    save_to_markdown(pgmap)

    logger.info('Script has finished running. Time elapsed: %s', datetime.datetime.now() - start_time)
    logger.info('-' * 80)
