from dotenv import load_dotenv
import os

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from gbpars.gbpars import settings

from youla import YoulaSpider
from insta import InstaSpider
from hh import HHSpider

from gbpars.gbpars import pipelines

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

load_dotenv('.env')

if __name__ == '__main__':
    crawl_settings = Settings()
    crawl_settings.setmodule(settings)
    crawl_proc = CrawlerProcess(settings=crawl_settings)
    # crawl_proc.crawl(YoulaSpider)
    # crawl_proc.crawl(HHSpider)
    crawl_proc.crawl(InstaSpider, login=os.getenv('USERNAME'), enc_password=os.getenv('ENC_PASSWORD'))
    crawl_proc.start()