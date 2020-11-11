# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GbparsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class HHVacancyItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    vacancy_name = scrapy.Field()
    vacancy_salary = scrapy.Field()
    description = scrapy.Field()
    skills = scrapy.Field()
    employer = scrapy.Field()

class HHEmployerItem(scrapy.Item):
    _id = scrapy.Field()
    employer_name = scrapy.Field()
    web_adress = scrapy.Field()
    field_of_activity = scrapy.Field()
    description = scrapy.Field()

class Insta(scrapy.Item):
    _id = scrapy.Field()
    date_parse = scrapy.Field()
    data = scrapy.Field()
    # img = scrapy.Field()

class InstaTag(Insta):
    pass


class InstaPost(Insta):
    pass

class InstaUser(Insta):
    pass

class InstaFollow(scrapy.Item):
    _id = scrapy.Field()
    date_parse = scrapy.Field()
    insta_user_name = scrapy.Field()
    insta_user_id = scrapy.Field()
    follow_name = scrapy.Field()
    follow_id = scrapy.Field()