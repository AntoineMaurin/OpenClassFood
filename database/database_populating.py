import sys
import mysql.connector

from database.database_request import DatabaseRequest
from database.tables import TABLES

sys.path.append("..")

"""This class creates the tables of the database and fills them with
categories and products from the API and researches from the user interface"""


class DatabasePopulating:
    def __init__(self):
        self.dbsetup = DatabaseRequest()

    def create_tables(self):
        for table_name in TABLES:
            table_description = TABLES[table_name]
            print("the table {} already exists".format(table_name))
            self.dbsetup.cursor.execute("DROP TABLE IF EXISTS %s" % table_name)
            print("table %s deleted" % table_name)
            try:
                print("Creating table {}: ".format(table_name))
                self.dbsetup.cursor.execute(table_description)
            except mysql.connector.Error as err:
                print(err.msg)
            else:
                print("OK")
        self.add_foreign_keys()

    def add_foreign_keys(self):
        try:
            self.dbsetup.cursor.execute(
                                    "ALTER TABLE `produit` "
                                    "ADD CONSTRAINT `fk_produit_categorie` "
                                    "FOREIGN KEY (`id_categorie`) "
                                    "REFERENCES `categorie` (`id`) "
                                    "ON DELETE CASCADE")
        except mysql.connector.Error as err:
            print(err.msg)
        try:
            self.dbsetup.cursor.execute(
                                    "ALTER TABLE `recherche` "
                                    "ADD CONSTRAINT `fk_id_produit_produit` "
                                    "FOREIGN KEY (`id_produit`) "
                                    "REFERENCES `produit` (`id`)")
        except mysql.connector.Error as err:
            print(err.msg)
        try:
            self.dbsetup.cursor.execute(
                                "ALTER TABLE `recherche` "
                                "ADD CONSTRAINT `fk_id_substitut_produit` "
                                "FOREIGN KEY (`id_substitut`) "
                                "REFERENCES `produit` (`id`)")
        except mysql.connector.Error as err:
            print(err.msg)

    def add_category(self, category):
        try:
            self.dbsetup.cursor.execute("INSERT INTO categorie (nom) "
                                        "VALUES ('%s')" % category.name)

            category_id_request = ("SELECT id FROM categorie "
                                   "WHERE nom = ('%s')" % category.name)

            self.dbsetup.cursor.execute(category_id_request)
        except mysql.connector.Error as err:
            print("problème lors de l'insertion des catégories")
            print(err.msg)

        try:
            for category_id in self.dbsetup.cursor:
                category.id = category_id[0]

            for product in category.products:
                elements = (product.name,
                            product.nutriscore,
                            product.description,
                            product.stores,
                            product.url,
                            category.id)
                add_aliment = ("INSERT INTO produit "
                               "(nom, nutriscore, description, magasin, "
                               " lien_openfoodfacts, id_categorie) "
                               "VALUES (%s, %s, %s, %s, %s, %s)")
                self.dbsetup.cursor.execute(add_aliment, elements)
            self.dbsetup.db.commit()
        except mysql.connector.Error as err:
            print("problème lors de l'insertion des produits")
            print(err.msg)

    def add_research(self, id_aliment, id_substitut):
        try:
            insert_research = ("INSERT INTO recherche "
                               "(date, id_produit, id_substitut) "
                               "VALUES (now(), %s, %s)" % (id_aliment,
                                                           id_substitut))
            self.dbsetup.cursor.execute(insert_research)
            self.dbsetup.db.commit()
            print("\nRecherche enregistrée !")
        except mysql.connector.Error as err:
            print(err.msg)

    def display_researches(self):
        full_request = ("SELECT prod.nom, prod.nutriscore, prod.description, "
                        "prod.magasin, prod.lien_openfoodfacts, "
                        "sub.nom, sub.nutriscore, "
                        "sub.description, sub.magasin, "
                        "sub.lien_openfoodfacts, date "
                        "FROM recherche "
                        "INNER JOIN produit as prod "
                        "ON recherche.id_produit = prod.id "
                        "INNER JOIN produit as sub "
                        "ON recherche.id_substitut = sub.id")

        self.dbsetup.cursor.execute(full_request)
        for id, elt in enumerate(self.dbsetup.cursor):
            print("\n", elt[10], "\n", id, "Produit recherché : ", *elt[0:5],
                  "\n", id, "Substitut trouvé  : ", *elt[5:10], sep=' - ')
