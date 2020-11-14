import scrapy
import json
import datetime as dt
from gbpars.gbpars.items import InstaUser, InstaFriends

class InstaKursach(scrapy.Spider):
    name = 'nearest_friends'
    allowed_domains = ['www.instagram.com']
    start_urls = ['https://www.instagram.com/']
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    query_hash ={}


    def __init__(self, login, enc_password, *args, **kwargs):
        self.login = login
        self.enc_password = enc_password
        super().__init__(*args, **kwargs)

        self.insta_user_1 = 'foxmalinart'
        self.insta_user_2 = 'dimarodovsky'

    @staticmethod
    def js_data_extract(response):
        script = response.xpath('//script[contains(text(), "window._sharedData =")]/text()').get()
        return json.loads(script.replace('window._sharedData = ', '')[:-1])

    def auth(self, response, **kwargs):
        try:
            js_data = self.js_data_extract(response)
            yield scrapy.FormRequest(
                self.login_url,
                method='POST',
                callback=self.parse,
                formdata={
                    'username': self.login,
                    'enc_password': self.enc_password
                },
                headers={'X-CSRFToken': js_data['config']['csrf_token']}
            )
        except AttributeError as e:
            if response.json().get('authenticated'):
                # for insta_user in self.insta_users:
                response.follow(
                    f'/{self.insta_user_1}/',
                    callback=self.insta_user_parse,
                    cb_kwargs={'insta_username_1': self.insta_user_1}
                )

    def insta_user_parse(self, response, **kwargs):
        insta_user_data = self.js_data_extract(response)['entry_data']['ProfilePage'][0]['graphql']['user']
        print(3)
        yield InstaUser(
            date_parse=dt.datetime.utcnow(),
            # data=insta_user_data
            insta_user_name_1 = kwargs['insta_username_1']
        )
        yield from self.url_user_followers(response, insta_user_data)

    def url_user_followers(self, response, insta_user_data):
        print(4)
