# pgmap = {"test": {"images": ["bla", "frist!", unichr(40960) + u'abcd' + unichr(1972)], "links": ["whatever", "second", "aaa"]}}
import unittest
import main
import logging
import const


class TestLinkExtract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html_string_valid = """
        <html>
        <a href="https://github.com/contact">Contact Support</a> &mdash;
        <a href="https://status.github.com">GitHub Status</a> &mdash;
        <a href="https://twitter.com/githubstatus">@githubstatus</a>
        <img alt="" class="wp-post-image" src="test.png">
        <img alt="" class="wp-post-image" src="rwar.png">
        </html>
        """
        cls.empty_html = """
        <html>
        </html>
        """

    def test_valid_links(self):
        valid_result = [u"https://github.com/contact", u"https://status.github.com",
                        u"https://twitter.com/githubstatus"]
        res = []
        for elem in main.extract_links(self.html_string_valid):
            res.append(elem)
        self.assertEqual(res, valid_result)

    def test_no_links(self):
        valid_result = []
        res = []
        for elem in main.extract_links(self.empty_html):
            res.append(elem)
        self.assertEqual(res, valid_result)

    def test_none(self):
        valid_result = []
        res = []
        for elem in main.extract_links(None):
            res.append(elem)
        self.assertEqual(res, valid_result)


if __name__ == '__main__':
    logger = logging.getLogger(const.LOGGER_NAME)
    unittest.main()
