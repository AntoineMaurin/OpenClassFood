import sys

sys.path.append("..")

import mysql.connector
from mysql.connector import errorcode

from API.data_from_api import DataFromApi
from database.database_setup import DatabaseSetup

class DatabaseInteraction:
    def __init__(self):
        self.data = DataFromApi()
        self.dbsetup = DatabaseSetup()
        self.dbsetup.connect('localhost', 'student', 'password')
        self.dbsetup.use_db('purbeurre')

    def get_categories(self):
        categories = []
        self.dbsetup.cursor.execute("SELECT nom FROM categorie")
        for category in self.dbsetup.cursor:
            categories.append(category)
        return categories

    def get_products_from_category(self, category):
        products = []
        self.dbsetup.cursor.execute("SELECT id FROM categorie "
                                    "WHERE nom = '{}'".format(category))
        for id in self.dbsetup.cursor:
            category_id = id[0]

        self.dbsetup.cursor.execute("SELECT "
                                    "id, nom, nutriscore, lien_openfoodfacts "
                                    "FROM aliment WHERE "
                                    "id_categorie = '{}'".format(category_id))

        for id, name, nutriscore, url_off in self.dbsetup.cursor:
            if name != '' and nutriscore != '':
                products.append((id, name, nutriscore, url_off))
        return products

    def get_substitute(self, product_name):
        words = product_name.split(" ")
        try:
          word_1 = words[1]
        except IndexError:
          word_1 = ''
        research = words[0] + ' ' + word_1

        self.dbsetup.cursor.execute("SELECT id, nom, nutriscore, description, "
                                    "magasin, lien_openfoodfacts "
                                    "FROM aliment "
                                    "WHERE nom LIKE '%{}%' "
                                    "AND nutriscore != '' "
                                    "ORDER BY nutriscore "
                                    "LIMIT 1".format(research))

        print("Substitut pour ce produit : ", research)

        for id, nom, nutri, desc, store, url in self.dbsetup.cursor:
            if nom == product_name:
                print("\nPas de produit plus sain que celui sélectionné")
            dataline = (id, nom, nutri, desc, store, url)

        return dataline

    def add_research(self, id_aliment, id_substitut):
        try:
            insert_research = ("INSERT INTO recherche "
                                        "(date, id_aliment, id_substitut) "
                                        "VALUES (now(), {}, {})".format(
                                        id_aliment, id_substitut
                                        ))
            self.dbsetup.cursor.execute(insert_research)
            self.dbsetup.db.commit()
            print("Added successfully in database !")
        except mysql.connector.Error as err:
            print(err.msg)

    def display_researches(self):
        full_request = ("SELECT recherche.date, recherche.id_aliment, "
                        "recherche.id_substitut, aliment.nom "
                        "FROM aliment INNER JOIN recherche "
                        "ON recherche.id_aliment = aliment.id "
                        "OR recherche.id_substitut = aliment.id")

        self.dbsetup.cursor.execute(full_request)
        print("Date et Heure", "Id aliment", "Id substitut", "Nom aliment",
              "Nom substitut", sep=' - ')
        data = []
        for elt in self.dbsetup.cursor:
            data.append(list(elt))
        try:
            for i, j in enumerate(data):
                if j[2] == data[i+1][2]:
                    data[i].append(data[i+1][3])
                    del data[i+1]
        except:
            pass
        for d in data:
            date = d[0]
            print("\n", date, d[1:], sep=' | ')
