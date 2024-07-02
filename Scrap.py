import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
from typing import List, NewType

Link = NewType('Link', str)

class Crawler:
    def __init__(self, root_link: Link):
        self.root_link = root_link
        self.urls = [root_link]
        self.visited_urls = set()

    def crawl(self):
        while len(self.urls) != 0:
            # get the page to visit from the list
            current_url = self.urls.pop()
            if current_url in self.visited_urls:
                continue
            print(current_url)
            self.visited_urls.add(current_url)
            response = requests.get(current_url)
            soup = BeautifulSoup(response.content, "html.parser")

            link_elements = soup.select("a[href]")
            for link_element in link_elements:
                url = link_element['href']
                if self.root_link in url:
                    self.urls.append(url)
        
        return self.visited_urls

class Scraping:
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

    def text_from_link(self, link:Link):
        response = requests.get(link)
        html = response.content
        return self.__text_from_html(html)

# print(Scraping().text_from_link('https://www.scrapingcourse.com/ecommerce/'))
