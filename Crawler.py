import requests
from typing import List, NewType
from bs4 import BeautifulSoup
import time
import logging


Link = NewType('Link', str)

LIMIT = 100
APPEND_OR_CREATE_MODE = "a+"
ValidFilename = NewType('ValidFilename', str)


class Crawler:
    def __init__(self, root_link: Link):
        self.root_link = root_link
        self.urls = [root_link]
        self.visited_urls = set()
        self.filename = self.__format_filename(self.root_link)
        logging.info('Links that have been visited:')

    def crawl(self):
        while len(self.urls) != 0 and len(self.visited_urls) <= LIMIT:
            # get the page to visit from the list
            current_url = self.urls.pop(0)
            if current_url in self.visited_urls:
                continue
            logging.debug(current_url)
            self.__process(current_url)
            self.__save(current_url)
        return self.visited_urls

    def __format_filename(self, filename:Link, prefix:str='', suffix:str='.txt') -> ValidFilename:
        # remove '/'s from file name as filename will be a link
        filename = filename.replace('//', '.')
        filename = filename.replace('/', '.')
        filename = filename.strip('.')
        filename = prefix + filename + suffix
        return filename
    
    def __save(self, content:str):
        with open(self.filename, APPEND_OR_CREATE_MODE) as file:
            file.write(content + "\n")

    def __process(self, current_url):
        self.visited_urls.add(current_url)
        try:
            response = requests.get(current_url)
            time.sleep(5)
        except Exception as exception:
            logging.debug(exception)
            logging.debug('pass')
            return
        soup = BeautifulSoup(response.content, "html.parser")

        link_elements = soup.select("a[href]")
        for link_element in link_elements:
            url = link_element['href']
            # do not process if external link
            if url.startswith(self.root_link):
                self.urls.append(url)

# crawler = Crawler("https://www.scrapingcourse.com/ecommerce/")
# local_url = crawler.crawl()
# print(local_url)