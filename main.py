from dotenv import load_dotenv
import os

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from gbpars.gbpars import settings

# from youla import YoulaSpider
# from insta import InstaSpider
# from insta_users import InstaSpiderUsers
from kursach import InstaKursach
# from hh import HHSpider

from gbpars.gbpars import pipelines

load_dotenv('.env')

if __name__ == '__main__':
    crawl_settings = Settings()
    crawl_settings.setmodule(settings)
    crawl_proc = CrawlerProcess(settings=crawl_settings)
    # crawl_proc.crawl(YoulaSpider)
    # crawl_proc.crawl(HHSpider)
    # crawl_proc.crawl(InstaSpider, login=os.getenv('USERNAME'), enc_password=os.getenv('ENC_PASSWORD'))
    # crawl_proc.crawl(InstaSpiderUsers, login=os.getenv('USERNAME'), enc_password=os.getenv('ENC_PASSWORD'))
    crawl_proc.crawl(InstaKursach, login=os.getenv('USERNAME'), enc_password=os.getenv('ENC_PASSWORD'))
    crawl_proc.start()