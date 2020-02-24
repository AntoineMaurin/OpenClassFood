import requests
import json
import sys

from database.database_populating import DatabasePopulating
from models.category import Category
from models.product import Product

sys.path.append("..")

"""This class sends requests to the urls in urls.txt to get the category of
products present on the url and these fields for each product :
product_name_fr, generic_name_fr, nutrition_grade_fr, stores, url
and then turn those fields into a Product object, and the category into a
Category object. When it's done for all products in a category, the category
object is sent to the class DatabasePopulating to fill the database with the
category and all the products it contains."""


class DataFromApi:

    def __init__(self):
        urls_file = open("API/urls.txt", "r")
        self.urls = [(line.strip()) for line in urls_file.readlines()]

        self.pop = DatabasePopulating()

    def get_category_from_url(self, url):
        end_url = url.split("/")[4]
        current_category = end_url.split(".")[0]
        return current_category

    def connect_to_API(self, incremented_url):
        try:
            response = requests.get(incremented_url,
                                    headers={'User-Agent':
                                             "OpenFoodRooms - "
                                             "windows/mac - "
                                             "Version 1.0"})
            # print(response.status_code)
            assert response.status_code < 400
        except AssertionError:
            print("Bad status code")
        else:
            pass

        json_response = json.loads(response.text)
        return json_response

    def request(self):
        for url in self.urls:
            category_name = self.get_category_from_url(url)
            category_object = Category(0, category_name)

            i = 0
            while True:
                i += 1
                incremented_url = url[:-5] + '/' + str(i) + '.json'
                print('url : ', incremented_url)

                json_response = self.connect_to_API(incremented_url)

                data = json_response["products"]

                if json_response["products"] == []:
                    break

                for elt in data:
                    product = self.build_product(elt, category_object)
                    category_object.add_product(product)
            self.pop.add_category(category_object)

    def build_product(self, dict, category_object):
        name = self.get_data('product_name_fr', dict)
        description = self.get_data('generic_name_fr', dict)
        nutriscore = self.get_data('nutrition_grade_fr', dict)
        stores = self.get_data('stores', dict)
        url_off = self.get_data('url', dict)
        product = Product(name, description, nutriscore, stores, url_off,
                          category_object)
        return product

    def get_data(self, key, dict):
        if key in dict:
            return dict[key].replace('\n', "")
        else:
            return ""
