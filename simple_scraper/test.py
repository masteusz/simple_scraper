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


class TestImageExtract(unittest.TestCase):
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
        valid_result = [u"test.png", u"rwar.png"]
        res = []
        for elem in main.extract_images(self.html_string_valid):
            res.append(elem)
        self.assertEqual(res, valid_result)

    def test_no_links(self):
        valid_result = []
        res = []
        for elem in main.extract_images(self.empty_html):
            res.append(elem)
        self.assertEqual(res, valid_result)

    def test_none(self):
        valid_result = []
        res = []
        for elem in main.extract_images(None):
            res.append(elem)
        self.assertEqual(res, valid_result)


class TestCleanLink(unittest.TestCase):
    def test_relative_link(self):
        valid_result = "https://test.com/testing_link"
        res = main.clean_link("/testing_link", "https://test.com/")
        self.assertEqual(res, valid_result)

    def test_absolute_link(self):
        self.assertEqual(main.clean_link("https://test.com/testing_link", "https://test.com/"), "https://test.com/testing_link")
        self.assertEqual(main.clean_link("http://test.com/testing_link", "http://test.com/"), "http://test.com/testing_link")

    def test_none(self):
        self.assertIsNone(main.clean_link(None))

    def test_mailto(self):
        self.assertIsNone(main.clean_link("mailto:test@test.com"))

if __name__ == '__main__':
    logger = logging.getLogger(const.LOGGER_NAME)
    unittest.main()
