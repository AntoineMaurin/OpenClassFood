import sys
import mysql.connector

from database.database_request import DatabaseRequest

sys.path.append("..")


class DatabasePopulating:
    def __init__(self):
        self.dbsetup = DatabaseRequest()

    def add_category(self, category):
        try:
            self.dbsetup.cursor.execute("INSERT INTO categorie (nom) "
                                        "VALUES ('%s')" %category.name)

            category_id_request = ("SELECT id FROM categorie "
                                   "WHERE nom = ('%s')" %category.name)

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
                add_aliment = ("INSERT INTO aliment "
                               "(nom, nutriscore, description, magasin, "
                               " lien_openfoodfacts, id_categorie) "
                               "VALUES (%s, %s, %s, %s, %s, %s)")
                self.dbsetup.cursor.execute(add_aliment, elements)
            self.dbsetup.db.commit()
        except mysql.connector.Error as err:
            print("problème lors de l'insertion des aliments")
            print(err.msg)

    def add_research(self, id_aliment, id_substitut):
        try:
            insert_research = ("INSERT INTO recherche "
                               "(date, id_aliment, id_substitut) "
                               "VALUES (now(), %s, %s)" %(id_aliment,
                                                          id_substitut))
            self.dbsetup.cursor.execute(insert_research)
            self.dbsetup.db.commit()
            print("\nRecherche enregistrée !")
        except mysql.connector.Error as err:
            print(err.msg)

    def display_researches(self):
        full_request = ("SELECT ali.nom, ali.nutriscore, ali.description, "
                        "ali.magasin, ali.lien_openfoodfacts, "
                        "sub.nom, sub.nutriscore, "
                        "sub.description, sub.magasin, "
                        "sub.lien_openfoodfacts, date "
                        "FROM recherche "
                        "INNER JOIN aliment as ali "
                        "ON recherche.id_aliment = ali.id "
                        "INNER JOIN aliment as sub "
                        "ON recherche.id_substitut = sub.id")

        self.dbsetup.cursor.execute(full_request)
        for id, elt in enumerate(self.dbsetup.cursor):
            print("\n", elt[10], "\n", id, "Produit recherché : ", *elt[0:5],
                  "\n", id, "Substitut trouvé  : ", *elt[5:10], sep=' - ')
