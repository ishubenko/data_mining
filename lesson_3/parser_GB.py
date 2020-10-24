import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from time import sleep
# from models import Post, Writer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models


class GeekBrainsParser:
    _headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0',
    }
    page = 1
    # engine = create_engine('sqlite:///gb_blog.db')
    # models.Base.metadata.create_all(bind=engine)
    # SessionMaker = sessionmaker(bind=)

    def __init__(self, start_url):
        self.start_url = start_url
        self._url = urlparse(start_url)
        self.engine = create_engine('sqlite:///gb_blog.db')
        models.Base.metadata.create_all(bind=self.engine)
        self.SessionMaker = sessionmaker(bind=self.engine)

    def _get_soup(self, url):
        response = requests.get(url, headers=self._headers)
        return BeautifulSoup(response.text, 'lxml')

    def parse(self):
        var_page = self.page
        # _url_page = self.start_url + '?page=' + str(self.var_page)
        soup = self._get_soup(self.start_url)

        while soup.find('div', attrs={'class':'post-items-wrapper'}).text:
            # soup = self._get_soup(_url_page)
            block_div_with_posts = soup.find('div', attrs={'class':'post-items-wrapper'})
            list_of_posts = block_div_with_posts.findChildren('a', attrs={'class': 'post-item__title h3 search_text'})

            for post in list_of_posts:
                post_url = f'{self._url.scheme}://{self._url.hostname}{post.attrs.get("href")}'
                output_data = self.post_parse(post_url)
                self.save_to_sqlite(output_data)
                sleep(0.5)
                print(output_data)

            var_page +=1
            url_page = self.start_url + '?page=' + str(var_page)
            soup = self._get_soup(url_page)

    def save_to_sqlite(self, output_data):
        db = self.SessionMaker()
        try:
            insert_author = models.Writer(
                name = output_data['author'],
                url = output_data['author_url']
            )
        except Exception:
            var_query = db.query(models.Writer.id).filter(models.Writer.url == output_data['author_url'])
            insert_author = var_query[0][0]

        insert_post = models.Post(
            url = output_data['post_url'],
            img_url = output_data['image_url'],
            writer = insert_author
        )
        db.add(insert_author, insert_post)
        # try:
        #     db.commit()
        # except Exception:
        #     db.rollback()
        #     var_query = db.query(models.Writer.id).filter(models.Writer.url == output_data['author_url'])
        #     # db.query(models.Writer.id).filter(models.Writer.url == )
        #     insert_post = models.Post(
        #         url=output_data['post_url'],
        #         img_url=output_data['image_url'],
        #         writer= var_query[0][0] # ID автора, который уже есть в базе
        #     )
        #     db.add(insert_post)
        db.commit()
        var = 555
        db.close()
        # pass

    def post_parse(self, post_url):
        soup_page = self._get_soup(post_url)
        post_template = {
            'post_url': post_url,
            'name_of_post': soup_page.find('article', attrs={'class':'col-sm-6 col-md-8 blogpost__article-wrapper'}).h1.text,
            # 'image_url': soup_page.find('div', attrs={'class':'blogpost-content content_text content js-mediator-article'}).img['src'],
            'date_time': soup_page.find('div', attrs={'class':'blogpost-date-views'}).time['datetime'],
            'author': soup_page.find('div', attrs={'itemprop':'author'}).text,
            'author_url': self.start_url[:-6] + soup_page.findChild('div', attrs={'class':'col-md-5 col-sm-12 col-lg-8 col-xs-12 padder-v'}).a['href'],
        }
        try:
            post_template['image_url'] = soup_page.find('div', attrs={'class':'blogpost-content content_text content js-mediator-article'}).img['src']
        except Exception:
            post_template['image_url'] = None

        return post_template


if __name__ == '__main__':
    url = 'https://geekbrains.ru/posts'
    parser = GeekBrainsParser(url)
    parser.parse()