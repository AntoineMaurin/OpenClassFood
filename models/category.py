import sys

sys.path.append("..")

import mysql.connector
from mysql.connector import errorcode

from database.database_setup import DatabaseSetup
from models.product import Product

class Category:
    def __init__(self, name):
        self.name = name
        self.id = ""
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def get_products(self):
        return self.products

    def connect_to_db(self):
        self.dbsetup = DatabaseSetup()
        self.dbsetup.connect('localhost', 'student', 'password')
        self.dbsetup.use_db('purbeurre')

    def get_all(cls):
        cls.connect_to_db()
        categories = []
        cls.dbsetup.cursor.execute("SELECT id, nom FROM categorie")
        for id, name in cls.dbsetup.cursor:
            category = Category(name)
            categories.append(category)
        return categories

    def get_products_from_category(cls, category):
        cls.connect_to_db()
        products = []
        get_category_id = ("SELECT id FROM categorie "
                                    "WHERE nom = '{}'".format(category.name))
        cls.dbsetup.cursor.execute(get_category_id)

        for id in cls.dbsetup.cursor:
            category_id = id[0]

        get_products_infos = ("SELECT id, nom, description, nutriscore,"
                              "magasin, lien_openfoodfacts, id_categorie "
                              "FROM aliment WHERE "
                              "id_categorie = {}".format(category_id))
        cls.dbsetup.cursor.execute(get_products_infos)

        for id, name, desc, ntsc, store, url_off, cat_id in cls.dbsetup.cursor:
            if name and ntsc:
                product_name = name
                product_description = desc
                product_nutriscore = ntsc
                product_store = store
                product_url = url_off
                product_category = cat_id
                product = Product(product_name, product_description,
                                  product_nutriscore, product_store,
                                  product_url, product_category)
                product.id = id
                products.append(product)
        return products
