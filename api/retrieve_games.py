import requests
import re
from bs4 import BeautifulSoup

def get_right_link(link):
    link = link.strip()
    if not link.startswith("https://") and not link.startswith("http://"):
        link = "http://" + link
    if link.startswith("https://"):
        link = link.replace("https://", "http://")
    link = re.sub(r"^http://(www\.)?", 'http://', link)
    return link

class GamesList:
    def __init__(self, results, current_page, next_page, last_page):
        self.results = results
        self.current_page = current_page
        self.next_page = next_page
        self.last_page = last_page

def retrieve_games(link):
    link = get_right_link(link)
    if not link.startswith("http://dedomil.net"):
        raise TypeError("link should be a Dedomil link")
    
    r = requests.get(link)

    soup = BeautifulSoup(r.text, 'html.parser')

    results = {}

    div_matches = soup.find_all('div', {'class': 'GMENU'})
    for div in div_matches:
        game_a_match = div.find('a', {'class': 'bluelink'})
        game_title = game_a_match.text
        game_title = game_title.replace("[39]", '\'')
        game_link = game_a_match.get('href')
        game_link = "http://dedomil.net" + game_link
        # game_span_match = div.find('span', {'class': 'DATE'})
        # if not game_span_match:
        #     date = None
        # else:
        #     date = game_span_match.text

        results[game_title] = {'link': game_link} #, 'date': date}

    current_page = re.search(r'/page/(\d+)', r.url)

    if current_page:
        current_page = [int(current_page.group(1)), r.url]

        pages_div_match = soup.find('div', {'class': 'PAGES'})
        if pages_div_match:
            last_page_a_match = pages_div_match.find('a', {'class': 'PAGES2'}, text="»»")
            if last_page_a_match:
                last_page_link = "http://dedomil.net" + last_page_a_match.get('href')
                splited = last_page_link.split("/")
                last_page = [int(splited[-1]), last_page_link]
            else:
                last_page = None

            next_page_a_match = pages_div_match.find('a', {'class': 'PAGES2'}, text='next»')
            if next_page_a_match:
                next_page_link = "http://dedomil.net" + next_page_a_match.get('href')
                splitted = next_page_link.split("/")
                next_page = [int(splitted[-1]), next_page_link]
            else:
                next_page = None
    else:
        current_page = None
        last_page = None
        next_page = None

    try:
        if not next_page:
            next_page = None
    except NameError:
        next_page = None
    try:
        if not last_page:
            last_page = None
    except NameError:
        last_page = None
    try:
        if not current_page:
            current_page = None
    except NameError:
        current_page = None
            
    return GamesList(results, current_page, next_page, last_page)
