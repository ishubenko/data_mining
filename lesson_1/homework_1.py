import requests
import json

url_categories = 'https://5ka.ru/api/v2/categories/'

response = requests.get(url_categories)
categories_json = response.json()
# params = {
#     'categories' : 732,
#     'records_per_page' : 20,
# }

# response = requests.get(url, params=params)

for categories in categories_json:
    current_category = categories['parent_group_code']
    # name_of_category = categories['parent_group_name']
    #number_category = current_category['parent_group_code']
    current_url = 'https://5ka.ru/api/v2/special_offers/?store=&records_per_page=12&page=1&categories=' + current_category + '&ordering=&price_promo__gte=&price_promo__lte=&search='
    # while current_url:
    response_per_category = requests.get(current_url)
    data = response_per_category.json()
    output = {
        'name of category' : categories['parent_group_name'],
        'code of category' : categories['parent_group_code'],
        'products' : data['results'],
    }
    with open( f'categories/{categories["parent_group_name"]}.json', 'w', encoding='UTF-8') as file_json_of_category:
        json.dump(output, file_json_of_category, ensure_ascii=False)

# class Parser5ka:
#     def __init__(self, start_url):
#         self.start_url = start_url
#
#     def parse(self, url=None):
#         if not url:
#             url= self.start_url
#
#         while url:
#             response = requests.get(url)
#             data: dict = response.json()
#             url = data['next']
#             for product in data['results']:
#                 self.save_to_json_file(product)
#
#
#     def save_to_json_file(self, product: dict):
#         with open( f'categories/{product["id"]}.json', 'w', encoding='UTF-8') as file:
#             json.dump(product, file)
#
#     # def make_categories(self, url):
#
# # with open(f'test.json', 'w', encoding='UTF-8') as json_file:
# #     json_file.write(response.text)
#     # json.load(json_file, response.text)
#
print('ok')