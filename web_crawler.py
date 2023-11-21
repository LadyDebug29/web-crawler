import json
from concurrent.futures import ThreadPoolExecutor
import os
import requests
from bs4 import BeautifulSoup


class WebCrawler:
    def __init__(self, url, depth):
        self.start_url = url
        self.__max_depth = depth
        self.__try_initialize_db()

    def get_result(self):
        return self.__result

    def __try_initialize_db(self):
        try:
            with open('links.txt', 'r') as file:
                self.__result = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.__result = {}

    def start_crawl(self):
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            executor.submit(self.crawl_url, self.start_url, self.__max_depth)

        with open('links.txt', 'w') as file:
            json.dump(self.__result, file, indent=4)

    def crawl_url(self, url, depth):
        if depth == 0:
            return

        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            self.__result[url] = {'links': []}
            for link in soup.find_all('a'):
                href = link.get('href')
                if href.startswith('http'):
                    self.__result[url]['links'].append(href)
                    self.crawl_url(href, depth - 1)
