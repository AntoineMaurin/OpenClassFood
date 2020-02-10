import sys

from database.database_setup import DatabaseSetup
from models.product import Product

sys.path.append("..")


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

    def get_all(self):
        self.connect_to_db()
        categories = []
        self.dbsetup.cursor.execute("SELECT id, nom FROM categorie")
        for id, name in self.dbsetup.cursor:
            category = Category(name)
            categories.append(category)
        return categories

    def get_products_from_category(self, category):
        self.connect_to_db()
        products = []
        get_category_id = ("SELECT id FROM categorie "
                           "WHERE nom = '{}'".format(category.name))
        self.dbsetup.cursor.execute(get_category_id)

        for id in self.dbsetup.cursor:
            category_id = id[0]

        get_products_infos = ("SELECT id, nom, description, nutriscore,"
                              "magasin, lien_openfoodfacts, id_categorie "
                              "FROM aliment WHERE "
                              "id_categorie = {}".format(category_id))
        self.dbsetup.cursor.execute(get_products_infos)

        for id, name, desc, ntsc, store, url, cat_id in self.dbsetup.cursor:
            if name and ntsc:
                product_name = name
                product_description = desc
                product_nutriscore = ntsc
                product_store = store
                product_url = url
                product_category = cat_id
                product = Product(product_name, product_description,
                                  product_nutriscore, product_store,
                                  product_url, product_category)
                product.id = id
                products.append(product)
        return products
