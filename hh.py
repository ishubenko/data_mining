import scrapy
from gbpars.gbpars.items import HHVacancyItem
from gbpars.gbpars.items import HHEmployerItem
from gbpars.gbpars.loaders import HHLoader
from gbpars.gbpars.loaders import HHLoaderEmployer

class HHSpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']
    xpath = {
        'vacancies': '//div[@class="vacancy-serp-item__row vacancy-serp-item__row_header"]//a/@href',
        'pagination':'//div[@data-qa="pager-block"]/a/@href',
    }
    xpath_vacancy = {
        'vacancy_name': '//div[@class="vacancy-title"]/h1[@data-qa="vacancy-title"]/text()',
        'vacancy_salary': '//p[@class="vacancy-salary"]//text()',
        'description': '//div[@data-qa="vacancy-description"]//text()',
        'skills': '//div[@class="bloko-tag-list"]//span[@class="bloko-tag__section bloko-tag__section_text"]/text()',
        'employer': '//a[@data-qa="vacancy-company-name"]/@href',
    }
    xpath_emloyer = {
        'employer_name':'//div[@class="company-header"]//span[@data-qa="company-header-title-name"]/text()',
        'description': '//div[@class="g-user-content"]//text()',
        'field_of_activity': '//div[@class="company-vacancies-group__title"]/span/text()',
        'web_adress': '//a[@data-qa="sidebar-company-site"]/@href',
    }

    def parse(self, response, **kwargs):
        for url in response.xpath(self.xpath['pagination']):
            yield response.follow(url, callback=self.parse)

        for url_vacancy in response.xpath(self.xpath['vacancies']):
            yield response.follow(url_vacancy, callback=self.vacancy_parse)

        print(1)

    def vacancy_parse(self, response, **kwargs):
        loader = HHLoader(response=response)
        loader.add_value('url', response.url)
        for key, value in self.xpath_vacancy.items():
            loader.add_xpath(key, value)

        yield loader.load_item()
        yield response.follow(response.xpath(self.xpath_vacancy['employer']).get(), callback=self.employer_parse)

    def employer_parse(self, response, **kwargs):
        loader = HHLoaderEmployer(response=response)
        # loader.add_value('url', response.url)
        for key, value in self.xpath_emloyer.items(): #xpath_vacancy!!!!!!!!!!!!!!!!!!
            loader.add_xpath(key, value)

        yield loader.load_item()
        # print(1)

        # vacancy_name = response.xpath(self.xpath['vacancy_name']).extract_first()
        # yield {
        #
        # }
