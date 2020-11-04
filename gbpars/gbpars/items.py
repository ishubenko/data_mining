# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class GbparsItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

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