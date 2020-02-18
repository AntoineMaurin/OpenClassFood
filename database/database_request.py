import mysql.connector

from database.tables import TABLES
from config import DB_CONFIG

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
            self.cursor.execute("USE %s" %name)
        except mysql.connector.Error as err:
            print("Can not USE purbeurre database\n", err.msg)

    # def create_database(self, name):
    #     try:
    #         self.cursor.execute("DROP DATABASE IF EXISTS {}".format(name))
    #         print("database dropped")
    #         self.cursor.execute("CREATE DATABASE {} "
    #                             "CHARACTER SET 'utf8'".format(name))
    #         print("database created successfully !")
    #         self.use_db(name)
    #         self.create_tables()
    #         print("all tables created successfully !")
    #     except mysql.connector.Error as err:
    #         print(err.msg)

    def create_tables(self):
        for table_name in TABLES:
            table_description = TABLES[table_name]
            print("the table {} already exists".format(table_name))
            self.cursor.execute("DROP TABLE IF EXISTS %s" %table_name)
            print("table %s deleted" %table_name)
            try:
                print("Creating table {}: ".format(table_name))
                self.cursor.execute(table_description)
            except mysql.connector.Error as err:
                print(err.msg)
            else:
                print("OK")
        self.add_foreign_keys()

    def add_foreign_keys(self):
        try:
            self.cursor.execute("ALTER TABLE `aliment` "
                                "ADD CONSTRAINT `fk_aliment_categorie` "
                                "FOREIGN KEY (`id_categorie`) "
                                "REFERENCES `categorie` (`id`) "
                                "ON DELETE CASCADE")
        except mysql.connector.Error as err:
            print(err.msg)
        try:
            self.cursor.execute("ALTER TABLE `recherche` "
                                "ADD CONSTRAINT `fk_id_aliment_aliment` "
                                "FOREIGN KEY (`id_aliment`) "
                                "REFERENCES `aliment` (`id`)")
        except mysql.connector.Error as err:
            print(err.msg)
        try:
            self.cursor.execute("ALTER TABLE `recherche` "
                                "ADD CONSTRAINT `fk_id_substitut_aliment` "
                                "FOREIGN KEY (`id_substitut`) "
                                "REFERENCES `aliment` (`id`)")
        except mysql.connector.Error as err:
            print(err.msg)

    def get_substitute(self, product):
        get_substitute_infos = ("SELECT id, nom, description, nutriscore,"
                                "magasin, lien_openfoodfacts, id_categorie "
                                "FROM aliment WHERE "
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
                              "FROM aliment WHERE "
                              "id_categorie = %s "
                              "AND nom != '' "
                              "AND nutriscore != '' "
                              "LIMIT 12" %category.id)
        self.cursor.execute(get_products_infos)
        for product in self.cursor:
            products.append(product)
        return products
