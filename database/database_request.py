import mysql.connector

from config import DB_CONFIG

"""This class makes requests on our database, and is used for example to get
the substitute of a product, get all categories, or get the products from a
specific category"""


class DatabaseRequest:

    def __init__(self):
        try:
            self.db = mysql.connector.connect(host=DB_CONFIG['host'],
                                              user=DB_CONFIG['user'],
                                              passwd=DB_CONFIG['password'])
            self.cursor = self.db.cursor()
            self.use_db(DB_CONFIG['db_name'])
        except mysql.connector.Error as err:
            print("Something went wrong in the connexion process\n", err.msg)
            self.db.close()

    def use_db(self, name):
        try:
            self.cursor.execute("USE %s" % name)
        except mysql.connector.Error as err:
            print("Can not USE %s database\n" % name, err.msg)

    def get_substitute(self, product):
        get_substitute_infos = ("SELECT id, nom, description, nutriscore,"
                                "magasin, lien_openfoodfacts, id_categorie "
                                "FROM produit WHERE "
                                "id_categorie = {} "
                                "AND nom != '' "
                                "AND nutriscore != '' "
                                "ORDER BY nutriscore "
                                "LIMIT 1".format(product.category.id))
        self.cursor.execute(get_substitute_infos)
        for sub_infos in self.cursor:
            return sub_infos

    def get_categories(self):
        categories = []
        self.cursor.execute("SELECT id, nom FROM categorie")
        for category in self.cursor:
            categories.append(category)
        return categories

    def get_products_from_category(self, category):
        products = []
        get_products_infos = ("SELECT id, nom, description, nutriscore,"
                              "magasin, lien_openfoodfacts "
                              "FROM produit WHERE "
                              "id_categorie = %s "
                              "AND nom != '' "
                              "AND nutriscore != '' "
                              "LIMIT 12" % category.id)
        self.cursor.execute(get_products_infos)
        for product in self.cursor:
            products.append(product)
        return products
