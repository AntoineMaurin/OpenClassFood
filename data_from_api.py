import requests
import json
import random

#User-Agent with the name of the app/service querying, system and the version
headers = {'User-Agent' : 'OpenFoodRooms - windows/mac - Version 1.0'}

class DataFromApi:

    def __init__(self):
        urls_file = open("urls.txt", "r")
        self.urls = [(line.strip()) for line in urls_file.readlines()]
        self.products = []

    def request(self, headers):
        i = 0
        while True:
            i += 1

            for url in self.urls:
                url = url[:-5] + '/' + str(i) + '.json'
                print('url : ', url)

                try:
                    response = requests.get(url, headers=headers)
                    print(response.status_code)
                    assert response.status_code < 400
                except AssertionError:
                    print("Bad status code")
                    break
                else:
                    pass

                json_response = json.loads(response.text)
                data = json_response["products"]

                for elt in data:
                    try :
                        # print('product_name_fr : ', elt["product_name_fr"])
                        # print('description : ', elt["generic_name_fr"])
                        # print('nutrition_score : ', elt["nutrition_grade_fr"])
                        # print('stores : ', elt["stores"])
                        # print('url : ', elt["url"])
                        self.products.append(list((
                                   elt["product_name_fr"],
                                   elt["generic_name_fr"],
                                   elt["nutrition_grade_fr"],
                                   elt["stores"],
                                   elt["url"])))

                    except KeyError:
                        # print('product_name_fr : ', '')
                        # print('description : ', '')
                        # print('nutrition_score : ', '')
                        # print('stores : ', '')
                        # print('url : ', '')
                        self.products.append(list(""))

            if json_response["products"] == []:
                print(json_response["products"])
                break

    def get_products(self):
        self.clean_products()
        for id, elt in enumerate(self.products):
            return self.products

    def show_random_product(self):
        try:
            return (random.choice(self.products))
        except IndexError:
            print("the list might be empty")

    def clean_products(self):
        for id, elt in enumerate(self.products):
            if elt == []:
                del self.products[id]

    def get_categories(self):
        categories = []
        for url in self.urls:
            end_url = url.split("/")[4]
            category = end_url.split(".")[0]
            categories.append(category)
        return categories
