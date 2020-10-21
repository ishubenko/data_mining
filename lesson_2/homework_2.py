import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
from pymongo import MongoClient
from time import sleep

# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'lxml')

class MagnitParser:
    _headers = {
        'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0',
    }
    _params = {
        'geo':'moskva',
    }

    def __init__(self, start_url):
        self.start_url = start_url
        self._url = urlparse(start_url)
        mongo_client = MongoClient('mongodb://localhost:27017')
        self.db = mongo_client['parse_10']

    def _get_soup(self, url):
        response = requests.get(url, headers=self._headers )
        return BeautifulSoup(response.text, 'lxml')

    def parse(self):
        soup = self._get_soup(self.start_url)
        catalog = soup.find('div', attrs={'class':'сatalogue__main'})
        products = catalog.findChildren('a', attrs={'class':'card-sale'})
        for product in products:
            if len(product.attrs.get('class')) > 3 or product.attrs.get('href')[0] != '/':
                continue
            product_url = f'{self._url.scheme}://{self._url.hostname}{product.attrs.get("href")}'
            product_soup = self._get_soup(product_url)
            product_data = self.get_product_structure(product_soup, product_url)
            self.save_to(product_data)
            # print(1)
        # print('ok')

    def get_product_structure(self, product_soup, url):
        months_to_digit = {
            'января': 1,
            'февраля': 2,
            'марта': 3,
            'апреля': 4,
            'мая': 5,
            'июня': 6,
            'июля': 7,
            'августа': 8,
            'сентября': 9,
            'октября': 10,
            'ноября': 11,
            'декабря': 12,
        }
        product_template = {
            'promo_name': ('div', 'action__name', 'text'),
            'product_name': ('div', 'action__title', 'text'),
            'old_price': ('div', 'label__price label__price_old', 'text'),
            'new_price': ('div', 'label__price label__price_new', 'text'),
            # 'image_url': ('img', 'alt', product['product_name'] ),
            'date_from': ('div', 'action__date', 'text'),
            'date_to': ('div', 'action__date', 'text'),
        }
        product = {'url':url}
        for key, value in product_template.items():
            try:
                product[key] = getattr(product_soup.find(value[0], attrs={'class': value[1]}), value[2])
            except Exception:
                product[key] = None
        product['promo_name'] = (product['promo_name']).split('\n')[1]
        try:
            product['old_price'] = float(
                ((product['old_price']).split('\n')[1]) + '.' + (product['old_price']).split('\n')[2])
        except Exception:
            product['old_price'] = None
        try:
            product['new_price'] = float(
                ((product['new_price']).split('\n')[1]) + '.' + (product['new_price']).split('\n')[2])
        except Exception:
            product['new_price'] = None
        product['date_from'] = datetime(year=2020,
                                        month=(months_to_digit[(product['date_from']).split(' ')[3]]),
                                        day=int((product['date_from']).split(' ')[2]))
        product['date_to'] = datetime(year=2020,
                                      month=(months_to_digit[((product['date_to']).split(' ')[6])[:-1]]),
                                      day=(int((product['date_to']).split(' ')[5])))
        try:
            product['image_url'] = self._url[0] + '://' + self._url[1] + product_soup.find(
                'img', attrs={'class':'action__image'})['data-src']
        except Exception:
            product['image_url'] = None
        #   product_soup.find('img', attrs={'class':'action__image'})['data-src']
        # month=(months_to_digit[(product['date_from']).split(' ')[3]])
        # product_soup.findChild('img', attrs={'alt':product['product_name']})
        sleep(0.5)
        return product

    def save_to(self, product_data):
        collection = self.db['magnit']
        collection.insert_one(product_data)
        pass

if __name__ == '__main__':
    url = 'https://magnit.ru/promo/?geo=moskva'
    parser = MagnitParser(url)
    parser.parse()