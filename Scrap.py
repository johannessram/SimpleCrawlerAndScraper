import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
from typing import List, NewType
import functools
import time
import logging


Link = NewType('Link', str)

LIMIT = 50
APPEND_OR_CREATE_MODE = "a+"

class Crawler:
    def __init__(self, root_link: Link):
        self.root_link = root_link
        self.urls = [root_link]
        self.visited_urls = set()

    def crawl(self):
        while len(self.urls) != 0 and len(self.visited_urls) <= LIMIT:
            # get the page to visit from the list
            current_url = self.urls.pop(0)
            if current_url in self.visited_urls:
                continue
            print(current_url)
            self.__process(current_url)
        return self.visited_urls


    def __process(self, current_url):
        self.visited_urls.add(current_url)
        try:
            response = requests.get(current_url)
            time.sleep(5)
        except Exception as exception:
            logging.info(exception)
            return
        soup = BeautifulSoup(response.content, "html.parser")

        link_elements = soup.select("a[href]")
        for link_element in link_elements:
            url = link_element['href']
            # do not process if external link
            if url.startswith(self.root_link):
                self.urls.append(url)


class Scraping:
    def __tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def save_txt(self, file_name:Link, content:str):
        # remove '/'s from file name as file_name will be a link
        file_name = file_name.replace('/', '.')
        file_name = file_name.strip('.')
        file_name = file_name + '.txt'

        with open(file_name, APPEND_OR_CREATE_MODE) as file:
            file.write(content)

    def __text_from_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        texts = soup.findAll(string=True)
        visible_texts = filter(self.__tag_visible, texts)  
        return u" ".join(t.strip() for t in visible_texts)

    def text_from_link(self, link:Link):
        response = requests.get(link)
        time.sleep(5)
        html = response.content
        visible_content = self.__text_from_html(html)
        self.save_txt(link, visible_content)
        return visible_content

# print(Scraping().text_from_link('https://www.scrapingcourse.com/ecommerce/'))
