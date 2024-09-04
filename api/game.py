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
    link = re.sub(r'/$', '', link)
    return link

def get_resolutions(link=None, id=None):
    if not link and not id:
        raise TypeError("link / id required.")
    
    if id and not id.isdecimal():
        raise TypeError("id should be a digit")
    
    if id:
        link = "http://dedomil.net/games/search/%d/screens" % id
    elif link:
        link = get_right_link(link)
    
    r = requests.get(link)
    
    soup = BeautifulSoup(r.text, 'html.parser')

    resolutions = {}

    gmenu_div_matches = soup.find_all('div', {'class': 'GMENU'})

    for div in gmenu_div_matches:
        a_match = div.find('a', {'class': 'bluelink'})
        res = a_match.text
        link = a_match['href']
        link = "http://dedomil.net" + link

        resolutions[res] = link

    return resolutions

class GetAppInfo:
    def __init__(self, link=None):
        r = requests.get(link)

        soup = BeautifulSoup(r.text, 'html.parser')
        self.soup = soup

        self.splash = self.get_splash()
        self.screenshots = self.get_screenshot()
        self.title, self.date, self.counter, self.vendor, self.description = self.get_infos()
        self.download_links = self.get_download_links()

    def get_splash(self):
        splash_div = self.soup.find('div', {'class': 'SPLASH'})
        if not splash_div:
            return None
        splash_a = splash_div.find('a')
        if not splash_div:
            return None
        splash_img = splash_a.find('img')
        if not splash_div:
            return None
        else:
            splash = splash_img.get('src')
            splash = "http://dedomil.net" + splash
            splash = splash.strip()
            return splash
    
    def get_screenshot(self):
        screenshot_div = self.soup.find('div', {'class': 'SECSCR'})
        if not screenshot_div:
            return None
        screenshot_a = screenshot_div.find('a', {'class': 'bluelink'})
        if not screenshot_a:
            return None
        screenshot = screenshot_a.get('href')
        if not screenshot:
            return None
        else:
            screenshot = "http://dedomil.net" + screenshot
            screenshot = screenshot.strip()
            return screenshot
    def get_infos(self):
        title_div = self.soup.find('div', {'class': 'NHRY'})
        if not title_div:
            title = None
        else:
            title = title_div.text
            if not title:
                title = None
            else:
                title = title.replace("[39]", '\'')

        infos = self.soup.find_all('div', {'class': 'OPIS'})
        
        for info in infos:
            info = info.text
            info = info.strip()
            if info.startswith("Added:"):
                date = re.search(r'Added: (.+)$', info)
                if not date:
                    date = None
                else:
                    date = date.group(1)
                    date = date.strip()
            elif info.startswith("Downloads:"):
                counter = re.search(r'Downloads: (.+)$', info)
                if not counter:
                    counter = None
                else:
                    counter = counter.group(1)
                    counter = counter.strip()
            elif info.startswith("Vendor:"):
                vendor = re.search(r'Vendor: (.+)$', info)
                if not vendor:
                    vendor = None
                else:
                    vendor = vendor.group(1)
                    vendor = vendor.strip()
                    vendor = vendor.replace("[39]", '\'')

        description_div = infos[-1].find_next_sibling('div')
        if description_div:
            description = description_div.text
            if description:
                description = '\n'.join(description.strip().splitlines())
                description = re.sub(r'^Description: ', '', description)
                description = description.replace("[39]", '\'')
            else:
                description = None
        else:
            description = None
        
        return (title, date, counter, vendor, description)
    
    def get_download_links(self):
        models_divs = self.soup.find_all('div', {'class': 'MODELS'})
        download_links = {}
        for div in models_divs:
            model_res = div.text.strip()
            
            res = div.find('b')
            if res:
                res = res.text
                model = re.sub(r'\(%s\)' % res, '', model_res)
                model = model.strip()
            else:
                continue
            
            download_links_div = div.find_next_sibling('div', {'class': 'LOAD'})
            a_jar_match = download_links_div.find('a', {'class': 'bluelink'}, text='JAR')
            if a_jar_match:
                link = a_jar_match.get('href')
                link = "http://dedomil.net" + link
                dl_type = "jar"
            else:
                a_zip_match = download_links_div.find('a', {'class': 'bluelink'}, text='download')
                if a_zip_match:
                    link = a_zip_match.get('href')
                    link = "http://dedomil.net" + link
                    dl_type = "zip"
                else:
                    link = None
            download_links[model] = {'res': res, 'link': link, 'type': dl_type}
        return download_links