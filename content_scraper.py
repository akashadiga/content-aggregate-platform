import requests
from bs4 import BeautifulSoup, Tag
import systemcheck
from typing import Dict, List
import time

url: str = "https://cryptonews.com/news/"
cryptonews_url = "https://cointelegraph.com/"
coindesk_url = "https://www.coindesk.com/"

def cryptonews_scraper(soup: BeautifulSoup) -> List[Dict[str, str]]:
    container = soup.find('section', {'class': 'category_contents_details'})
    articles: List[Dict[str,str]] = []
    if container is not None and isinstance(container, Tag):
        for news in container.find_all('article'):
            article = news.find('a', {'class': 'article__title'})
            if article:
                articles.append({'title': article.text, 'url': article.get('href')})
    return articles
def cointelegraph_scraper(soup: BeautifulSoup) -> List[Dict[str, str]]:
    container = soup.find('ul', {'class': 'posts-listing__list'})
    articles: List[Dict[str,str]] = []
    if container is not None and isinstance(container, Tag):
        for news in container.find_all('li'):
            article_header = news.find("header", {'class': 'post-card__header'})
            if article_header is not None:
                article = article_header.find('a')
                articles.append({'title': article.text, 'url': article.get('href')})
    return articles
def coindesk_scraper(soup: BeautifulSoup) -> List[Dict[str, str]]:
    container = soup.find('div', {'class': 'leaderboardstyles__Wrapper-lxd6ux-0'})
    articles: List[Dict[str,str]] = []
    if container is not None and isinstance(container, Tag):
        container.find("section") # import here
        for article in container.find_all('a', {'class': 'card-title'}):
            articles.append({'title': article.text, 'url': article.get('href')})
    return articles

def make_soup(url: str) -> BeautifulSoup:
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(r.content, 'html.parser')
    time.sleep(2)
    return soup

if __name__ == "__main__":
    print("###############################")
    # https://cryptonews.com/news/
    soup = make_soup(url)
    print(cryptonews_scraper(soup))

    print("###############################")
    # https://cointelegraph.com/
    soup = make_soup(cryptonews_url)
    print(cointelegraph_scraper(soup))

    print("###############################")
    # https://www.coindesk.com/ 
    soup = make_soup(coindesk_url)
    print(soup)
    print(coindesk_scraper(soup))