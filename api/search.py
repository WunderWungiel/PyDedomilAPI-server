import re
from .retrieve_games import retrieve_games

def get_right_link(link):
    link = link.strip()
    if not link.startswith("https://") and not link.startswith("http://"):
        link = "http://" + link
    if link.startswith("https://"):
        link = link.replace("https://", "http://")
    link = re.sub(r"^http://(www\.)?", 'http://', link)
    return link

def search(query):
    if len(query) <= 3:
        raise Exception("Search query should be 3-letters long or more.")
    
    link = "http://dedomil.net/games/search/%s/page/1" % query
    results = retrieve_games(link)
    return results