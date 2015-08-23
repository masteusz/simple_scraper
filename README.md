# simple_scraper

Simple web scraper.

## Usage: 
`python main.py`

Domain to be crawled is set in `const.py` file.

Returns a Markdown file containing map of internal links within given webpage.

## Libraries required:
* beautifulsoup
* requests

## TODO:
* Add CLI
* Improve link filtering
* Change queue mechanism from list to something thread-safe
* Implement concurrency
* Add other output possibilities