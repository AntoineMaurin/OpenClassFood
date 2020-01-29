from database_only import DatabaseSetup
from data_from_api import DataFromApi

import mysql.connector

from mysql.connector import errorcode

class DatabasePopulating:
    def __init__(self):
        self.data = DataFromApi()
        self.dbonly = DatabaseSetup('localhost', 'student', 'password')
        self.dbonly.create_database('purbeurre')
        self.dbonly.show_databases()
        self.dbonly.show_tables()

    def show_categories(self):
        for data in self.data.get_categories():
            print(data)

    def populate_categorie_field(self):
        for data in self.data.get_categories():
            try:
                add_categories = ("INSERT INTO categorie (nom) "
                   "VALUES ('{}')".format(data))

                self.dbonly.cursor.execute(add_categories)
            except mysql.connector.Error as err:
                print("problème lors de l'insertion des catégories")
                print(err.msg)

        self.dbonly.db.commit()

    def show_table_content(self, table_name):
        show_content_request = ("SELECT * FROM {}".format(table_name))
        self.dbonly.cursor.execute(show_content_request)

        for id, elt in enumerate(self.dbonly.cursor):
            print(id, elt)

    def populate_aliment_field(self):
        for id, aliment in enumerate(self.data.get_products()):
            print("id : ", id, aliment)
            elements = (aliment[0], aliment[1], aliment[2], aliment[3], aliment[4])
            try:
                add_aliment = (
                "INSERT INTO aliment "
                "(nom, description, nutriscore, magasin, lien_openfoodfacts) "
                "VALUES (%s, %s, %s, %s, %s)"
                )
                self.dbonly.cursor.execute(add_aliment, elements)
            except mysql.connector.Error as err:
                print("problème lors de l'insertion des aliments")
                print(err.msg)
            except IndexError:
                print("IndexError")

        self.dbonly.db.commit()


headers = {'User-Agent' : 'OpenFoodRooms - windows/mac - Version 1.0'}

pop = DatabasePopulating()

pop.data.request(headers)

pop.show_categories()
pop.populate_categorie_field()
pop.show_table_content('categorie')
pop.populate_aliment_field()
pop.show_table_content('aliment')
