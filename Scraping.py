import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
from typing import List, NewType
import functools
import time
import logging


Link = NewType('Link', str)
APPEND_OR_CREATE_MODE = "a+"


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

print(Scraping().text_from_link('https://www.scrapingcourse.com/ecommerce/'))
