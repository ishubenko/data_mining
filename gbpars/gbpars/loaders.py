from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader
from gbpars.gbpars.items import HHVacancyItem
from gbpars.gbpars.items import HHEmployerItem
import re

# def get_specification(items):
#     result = {}
#     for item in items:
#         if None not in items:
#             result.update(item)
#     return result

def description_rewrite(items):
    return ''.join(items)

class HHLoader(ItemLoader):
    default_item_class = HHVacancyItem
    title_out = TakeFirst()
    url_out = TakeFirst()
    description_in = ''.join
    description_out = TakeFirst()
    vacancy_salary_in = ''.join
    vacancy_salary_out = TakeFirst()

class HHLoaderEmployer(ItemLoader):
    default_item_class = HHEmployerItem
    title_out = TakeFirst()
    web_adress = TakeFirst()
    description_in = ''.join
    description_out = TakeFirst()
    field_of_activity = TakeFirst()
    # field_of_activity = ''.join
    # vacancy_salary_out = TakeFirst()