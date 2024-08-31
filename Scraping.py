import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
from typing import List, NewType
import functools
import time
import logging


Link = NewType('Link', str)
APPEND_OR_CREATE_MODE = "a+"
ValidFilename = NewType('ValidFilename', str)


class Scraping:
    def __format_filename(self, filename:Link, prefix:str='', suffix:str='.dump.txt') -> ValidFilename:
        # remove '/'s from file name as filename will be a link
        filename = filename.replace('//', '')
        filename = filename.replace('/', '.')
        filename = filename.strip('.')
        filename = prefix + filename + suffix
        return filename
    
    def __save(self, filename, content:str):
        with open(self.filename, APPEND_OR_CREATE_MODE) as file:
            file.write(content + "\n")

    def __tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True


    def __text_from_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        texts = soup.findAll(string=True)
        visible_texts = filter(self.__tag_visible, texts)  
        return u" ".join(t.strip() for t in visible_texts)

    def text_from_link(self, link:Link, filename:str=None):
        if not filename:
            filename = self.__format_filename(link)
        self.filename = filename

        response = requests.get(link)
        time.sleep(5)
        html = response.content
        visible_content = self.__text_from_html(html)
        self.__save(filename, visible_content)
        return visible_content

print(Scraping().text_from_link('https://www.scrapingcourse.com/ecommerce/'))
