import sys
import mysql.connector

from database_setup import DatabaseSetup
from mysql.connector import errorcode

sys.path.append('../API')

from data_from_api import *

class DatabasePopulating:
    def __init__(self):
        self.data = DataFromApi()
        self.dbsetup = DatabaseSetup()
        self.dbsetup.connect('localhost', 'student', 'password')
        self.dbsetup.use_db('purbeurre')

    def populate(self):
        for category in self.data.get_categories():
            category_id = self.add_category_in_db(category)
            print(category_id)
            for product in category.products:
                self.add_product_in_db(product, category_id)

    def add_category_in_db(self, category):
        try:
            self.dbsetup.cursor.execute("INSERT INTO categorie (nom) "
               "VALUES ('{}')".format(category.name))

            category_id_request = ("SELECT id FROM categorie "
                "WHERE nom = ('{}')".format(category.name))

            self.dbsetup.cursor.execute(category_id_request)

            for category_id in self.dbsetup.cursor:
                category_id = category_id[0]

            print('added_category_id : ', category_id)
            return category_id
            self.dbsetup.db.commit()
        except mysql.connector.Error as err:
            print("problème lors de l'insertion des catégories")
            print(err.msg)

    def add_product_in_db(self, product, category_id):
        try:
            elements = (product.name,
                        product.nutriscore,
                        product.description,
                        product.stores,
                        product.url,
                        category_id)
            print('elements = ', elements)
            add_aliment = (
            "INSERT INTO aliment "
            "(nom, nutriscore, description, magasin, lien_openfoodfacts, id_categorie) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
            )
            self.dbsetup.cursor.execute(add_aliment, elements)
            self.dbsetup.db.commit()
        except mysql.connector.Error as err:
            print("problème lors de l'insertion des aliments")
            print(err.msg)
        except IndexError:
            print("IndexError")

    def show_categories(self):
        for data in self.data.get_categories():
            print(data)

    def show_table_content(self, table_name):
        show_content_request = ("SELECT * FROM {}".format(table_name))
        self.dbsetup.cursor.execute(show_content_request)

        for id, elt in enumerate(self.dbsetup.cursor):
            print(id, elt)
