import requests
import json
import sys

from database.database_populating import DatabasePopulating
from models.category import Category
from models.product import Product

sys.path.append("..")


class DataFromApi:

    def __init__(self):
        urls_file = open("API/urls.txt", "r")
        self.urls = [(line.strip()) for line in urls_file.readlines()]

        self.pop = DatabasePopulating()
        self.categories = []

    def request(self):
        for url in self.urls:
            end_url = url.split("/")[4]
            current_category = end_url.split(".")[0]

            category_object = Category(current_category)
            self.categories.append(category_object)

            i = 0
            while True:
                i += 1
                incremented_url = url[:-5] + '/' + str(i) + '.json'
                print('url : ', incremented_url)

                try:
                    response = requests.get(incremented_url,
                                            headers={'User-Agent':
                                                     "OpenFoodRooms - "
                                                     "windows/mac - "
                                                     "Version 1.0"})
                    print(response.status_code)
                    assert response.status_code < 400
                except AssertionError:
                    print("Bad status code")
                    break
                else:
                    pass

                json_response = json.loads(response.text)
                data = json_response["products"]

                if json_response["products"] == []:
                    break

                for elt in data:
                    name = self.get_data('product_name_fr', elt)
                    description = self.get_data('generic_name_fr', elt)
                    nutriscore = self.get_data('nutrition_grade_fr', elt)
                    stores = self.get_data('stores', elt)
                    url_off = self.get_data('url', elt)

                    product = Product(name, description, nutriscore, stores,
                                      url_off, category_object)
                    category_object.add_product(product)
            # for id, product in enumerate(category_object.products):
            #     print(id, product.name)
            self.pop.add_category(category_object)

    def get_data(self, key, dic):
        if key in dic:
            return dic[key]
        else:
            return ""

    def get_categories(self):
        return self.categories

    # def get_products(self):
    #     while [] in self.products:
    #         self.products.remove([])
    #     return self.products
