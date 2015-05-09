import urllib.request
from bs4 import BeautifulSoup

PUBLISHER_IDS = {
    "Dark Horse Comics": "914",
    "DC Comics": "915",
    "IDW Publishing": "916",
    "Image Comics": "917",
    "Marvel Comics": "918",
}

BASE_URL = 'http://www.previewsworld.com/'

class ImageFinderError(Exception):
    pass

class ConnectionError(Exception):
    pass

def get_release_location(publisher, code):
    if not publisher in PUBLISHER_IDS.keys():
        raise ValueError('invalid publisher')
    base_release_url = BASE_URL + 'Home/1/1/71/'
    return base_release_url + PUBLISHER_IDS[publisher] + '?stockItemID=' + code

def get_image_location(publisher, code):
    url = get_release_location(publisher, code)
    try:
        f = urllib.request.urlopen(url)
    except Exception as e:
        raise ConnectionError('cannot connect to PreviewsWorld') from e
    soup = BeautifulSoup(f.read())
    image_container = soup.find(class_='StockCodeImage')
    if not image_container:
        raise ImageFinderError('no image container found')
    image = image_container.find('img')
    if not image:
        raise ImageFinderError('no image found')
    image_location = image['src']
    if not image_location:
        raise ImageFinderError('image src is empty')
    return BASE_URL + image_location
