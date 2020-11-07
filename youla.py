import scrapy
from pymongo import MongoClient
import re


class YoulaSpider(scrapy.Spider):
    name = 'youla'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/']
    xpath = {
        'brands': '//div[@class="TransportMainFilters_brandsList__2tIkv"]//a[@class="blackLink"]/@href',
        'ads': '//div[@id="serp"]//article//a[@data-target="serp-snippet-title"]/@href',
        'pagination': '//div[contains(@class, "Paginator_block")]/a/@href',
        'name': '//div[contains(@class, "AdvertCard_advertTitle")]/text()',
        'images': '//div[contains(@class, "PhotoGallery_block")]//img/@src',
        'characteristics':'//div[@class="AdvertCard_specs__2FEHc"]//div[contains(@data-target,"advert-info-")]//text()',
        'description_full': '//div[contains(@data-target, "advert-info-descriptionFull")]/text()'
    }
    # db_client = MongoClient('mongodb://localhost:27017')

    def parse(self, response, **kwargs):
        for url in response.xpath(self.xpath['brands']):
            yield response.follow(url, callback=self.brand_parse)
        # brands_auto = response.css('.TransportMainFilters_brandsList__2tIkv a.blackLink')
        # for brand_number in range(len(brands_auto)):
        #     brand_url = brands_auto[brand_number].attrib['href']
        #     # print(brand_url)
        #     self.data_from_ad(brand_url, response)
        pass

    def brand_parse(self, response, **kwargs):
        for url in response.xpath(self.xpath['pagination']):
            yield response.follow(url, callback=self.brand_parse)

        for url in response.xpath(self.xpath['ads']):
            yield response.follow(url, callback=self.ads_parse)

    def ads_parse(self, response, **kwargs):
        specifications = {
            itm.xpath('div[1]/text()').get() : itm.xpath('div[2]/text()').get() or itm.xpath('div[2]/a/text()').get() for
            itm in response.xpath('//div[contains(@class, "AdvertCard_specs")]//div[contains(@class, "AdvertSpecs")]')
            if itm.xpath('div[1]/text()').get()
        }

        name = response.xpath(self.xpath['name']).extract_first()
        images = response.xpath(self.xpath['images']).extract()
        characteristics = response.xpath(self.xpath['characteristics']).extract()
        description_full = response.xpath(self.xpath['description_full']).extract()
        author = self.js_decoder_author(response)

        # save to mongo
        # collection = self.db_client['parse_10'][self.name]
        # collection.insert_one(
        #     {'title': name,
        #     'images': images,
        #     'specifications': specifications,
        #     # 'characteristics': characteristics,
        #     'description': description_full,
        #     'author': author,
        #     }
        # )
        yield {'title': name,
            'images': images,
            'specifications': specifications,
            # 'characteristics': characteristics,
            'description': description_full,
            'author': author,
            }

    def js_decoder_author(self, response):
        script = response.xpath('//script[contains(text(), "window.transitState =")]/text()').get()
        re_str = re.compile(r"youlaId%22%2C%22([0-9|a-zA-Z]+)%22%2C%22avatar")
        # re.compile()
        result = re.findall(re_str, script)
        return f'https://youla.ru/user/{result[0]}' if result else None