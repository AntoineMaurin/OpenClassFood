import sys

sys.path.append("..")

import mysql.connector
from mysql.connector import errorcode

from models.category import Category
from models.product import Product

class UiInteraction:
    def __init__(self):
        self.cat = Category('')

    def get_categories(self):
        categories = self.cat.get_all()
        return categories

    def get_products(self, category):
        products = self.cat.get_products_from_category(category)
        return products

    def get_substitute(self, product):
        self.product = product
        substitute = product.get_substitute(product.category)
        return substitute
