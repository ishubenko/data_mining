import scrapy
import json
import datetime as dt
from gbpars.gbpars.items import InstaUser, InstaFriends, TemporaryInfo

class InstaKursach(scrapy.Spider):
    name = 'nearest_friends'
    allowed_domains = ['www.instagram.com']
    start_urls = ['https://www.instagram.com/']
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    query_hash ={
        'followers': 'c76146de99bb02f6415203be841dd25a'
    }


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

    def parse(self, response, **kwargs):
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
                yield response.follow(f'/{self.insta_user_1}/', callback=self.insta_user_parse, cb_kwargs={'param': self.insta_user_1})

    def insta_user_parse(self, response, **kwargs):
        insta_user_data = self.js_data_extract(response)['entry_data']['ProfilePage'][0]['graphql']['user']
        yield InstaFriends(
            date_parse=dt.datetime.utcnow(),
            insta_user_name_1 = kwargs['param']
        )
        yield from self.url_user_followers(response, insta_user_data)

    def url_user_followers(self, response, insta_user_data, variables=None):
        if not variables:
            variables = {
                'id': insta_user_data['id'],
                'first': 100
            }
        url = f'/graphql/query/?query_hash={self.query_hash["followers"]}&variables={json.dumps(variables)}'
        yield response.follow(url, callback=self.followers_parse, cb_kwargs={'insta_user_data': insta_user_data})

    def followers_parse(self, response, insta_user_data):
        if b'application/json' in response.headers['Content-Type']:
            data = response.json()
            yield from self.get_followers_item(insta_user_data,
                                            data['data']['user']['edge_followed_by']['edges'])
            if data['data']['user']['edge_followed_by']['page_info']['has_next_page']:
                variables = {
                    'id': insta_user_data['id'],
                    'first': 100,
                    'after': data['data']['user']['edge_followed_by']['page_info']['end_cursor'],
                }
                yield from self.url_user_followers(response, insta_user_data, variables)

    def get_followers_item(self, insta_user_data, followers_users_data):
        list_of_friends = []
        for user in followers_users_data:
            if user['node']['username'] == self.insta_user_2:
                yield
            list_of_friends.append(user['node']['username'])
            yield TemporaryInfo(
                insta_user_name_1=insta_user_data['username'],
                list_of_friends= user['node']['username']
            )

    def output(self,):
        print('ВАУ')