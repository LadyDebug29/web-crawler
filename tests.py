import unittest
import json
import os
from main import try_make_directory
from web_crawler import WebCrawler


class TestWebCrawler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try_make_directory('tests_links')
        os.chdir('tests_links')

    def setUp(self):
        self.url = 'https://example.com'
        self.depth = 2
        self.web_crawler = WebCrawler(self.url, self.depth)

    def test_try_initialize_db_invalid_json(self):
        with open('links.txt', 'w') as file:
            file.write('Invalid JSON')
        self.web_crawler._WebCrawler__try_initialize_db()
        self.assertEqual(self.web_crawler._WebCrawler__result, {})

    def test_try_initialize_db_success(self):
        self.web_crawler._WebCrawler__try_initialize_db()
        self.assertEqual(self.web_crawler._WebCrawler__result, {})

    def test_start_crawl(self):
        self.web_crawler.start_crawl()
        with open('links.txt', 'r') as file:
            result = json.load(file)
        self.assertEqual(self.web_crawler._WebCrawler__result, result)

    def test_crawl_url_depth_zero(self):
        url = self.url
        depth = 0
        self.web_crawler.crawl_url(url, depth)
        self.assertEqual(self.web_crawler._WebCrawler__result, {})

    def test_crawl_url_success(self):
        url = self.url
        depth = 1

        self.web_crawler.crawl_url(url, depth)

        expected_result = {
            url: {'links': ['https://www.iana.org/domains/example']}
        }
        self.assertEqual(self.web_crawler._WebCrawler__result, expected_result)

    def test_crawl_url_invalid_status_code(self):
        url = 'https://example.com/404'
        depth = 1
        self.web_crawler.crawl_url(url, depth)
        self.assertEqual(self.web_crawler._WebCrawler__result, {})


if __name__ == '__main__':
    unittest.main()
