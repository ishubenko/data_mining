import scrapy
import json
import datetime as dt
from gbpars.gbpars.items import InstaUser, InstaFollow


class InstaSpiderUsers(scrapy.Spider):
    name = 'insta_users'
    allowed_domains = ['www.instagram.com']
    start_urls = ['https://www.instagram.com/']
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    # api_url = '/graphql/query/'
    query_hash = {
        # 'followers': 'c76146de99bb02f6415203be841dd25a',
        # 'followings': 'd04b0a864b4b54837c0d870b0e77e076',
        'followers': 'd04b0a864b4b54837c0d870b0e77e076',
        'followings': 'c76146de99bb02f6415203be841dd25a',
    }
    edge_follow = {
        'edge_follow': 'edge_follow',
        'edge_followed_by': 'edge_followed_by',
    }

    def __init__(self, login, enc_password, *args, **kwargs):
        self.insta_users = [
            'schekinaan',
            # 'foxmalinart',
        ]
        self.login = login
        self.enc_password = enc_password
        super().__init__(*args, **kwargs)

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
                for insta_user in self.insta_users:
                    yield response.follow(f'/{insta_user}/', callback=self.insta_user_parse, cb_kwargs={'param': insta_user})
                                          # cb_kwargs={'param': insta_user}

    def insta_user_parse(self, response, **kwargs):
        insta_user_data = self.js_data_extract(response)['entry_data']['ProfilePage'][0]['graphql']['user']
        insta_user = kwargs['param']
        print(insta_user)
        yield InstaUser(
            date_parse = dt.datetime.utcnow(),
            data = insta_user_data
        )
        yield from self.url_user_followers(response, insta_user_data)

    def url_user_followers(self, response, insta_user_data, variables=None):
        if not variables:
            variables = {
                'id': insta_user_data['id'],
                # 'include_reel': 'true',
                # 'fetch_mutual': 'false',
                'first': 100
            }
        url = f'/graphql/query/?query_hash={self.query_hash["followers"]}&variables={json.dumps(variables)}'
        yield response.follow(url, callback=self.followers_parse, cb_kwargs={'insta_user_data': insta_user_data})

    def followers_parse(self, response, insta_user_data):
        if b'application/json' in response.headers['Content-Type']:
            data = response.json()
            yield from self.get_follow_item(insta_user_data, data['data']['user'][self.edge_follow['edge_follow']]['edges'])
            if data['data']['user'][self.edge_follow['edge_follow']]['page_info']['has_next_page']:
                variables = {
                    'id': insta_user_data['id'],
                    'first': 100,
                    'after': data['data']['user'][self.edge_follow['edge_follow']]['page_info']['end_cursor'],
                }
                yield from self.url_user_followers(response, insta_user_data, variables)

    def get_follow_item(self, insta_user_data, follow_users_data):
        for user in follow_users_data:
            yield InstaFollow(
                insta_user_id=insta_user_data['id'],
                insta_user_name=insta_user_data['username'],
                follow_id=user['node']['id'],
                follow_name=user['node']['username']
            )
            yield InstaUser(
                date_parse=dt.datetime.utcnow(),
                data=user['node']
            )

    @staticmethod
    def js_data_extract(response):
        script = response.xpath('//script[contains(text(), "window._sharedData =")]/text()').get()
        return json.loads(script.replace('window._sharedData = ', '')[:-1])
