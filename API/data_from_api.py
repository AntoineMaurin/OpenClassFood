import requests
import json
import random

from API.category_and_products import Category, Product

class DataFromApi:

    def __init__(self):
        urls_file = open("API/urls.txt", "r")
        self.urls = [(line.strip()) for line in urls_file.readlines()]

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
                    headers={
                    'User-Agent' : 'OpenFoodRooms - windows/mac - Version 1.0'
                    })
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
                    print(json_response["products"])
                    break

                for elt in data:
                    try :
                        name = (elt["product_name_fr"])
                    except:
                        name = ""
                    try :
                        description = (elt["generic_name_fr"])
                    except:
                        description = ""
                    try :
                        nutriscore = (elt["nutrition_grade_fr"])
                    except:
                        nutriscore = ""
                    try :
                        stores = (elt["stores"])
                    except:
                        stores = ""
                    try :
                        url_off = (elt["url"])
                    except:
                        url_off = ""

                    product = Product(name, description, nutriscore, stores, url_off)
                    category_object.add_product(product)
                    product.category = category_object.name

    # def get_products(self):
    #     while [] in self.products:
    #         self.products.remove([])
    #     return self.products

    def get_categories(self):
        return self.categories
