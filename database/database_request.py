import mysql.connector

from database.tables import TABLES


class DatabaseRequest:

    def __init__(self):
        try:
            self.db = mysql.connector.connect(host='localhost',
                                              user='student',
                                              passwd='password',
                                              buffered=True)
            self.cursor = self.db.cursor()
            self.use_db('purbeurre')
        except mysql.connector.Error as err:
            print("Something went wrong in the connexion process\n", err.msg)
            self.db.close()

    def use_db(self, name):
        try:
            self.cursor.execute("USE {}".format(name))
        except mysql.connector.Error as err:
            print("Can not USE purbeurre database\n", err.msg)

    def create_database(self, name):
        try:
            self.cursor.execute("DROP DATABASE IF EXISTS purbeurre")
            print("database dropped")
            self.cursor.execute("CREATE DATABASE purbeurre "
                                "CHARACTER SET 'utf8'")
            print("database created successfully !")
            self.use_db(name)
            self.create_tables()
            print("all tables created successfully !")
        except mysql.connector.Error as err:
            print(err.msg)

    def does_db_exist(self, name):
        databases = []
        self.cursor.execute("SHOW DATABASES")
        for db in self.cursor:
            db = db[0]
            databases.append(db)

        print('databases : ', databases)
        return name in databases

    def does_tb_exist(self, table):
        tables = []
        self.cursor.execute("SHOW TABLES")
        for tb in self.cursor:
            tb = tb[0]
            tables.append(tb)

        print('tables : ', tables)
        return table in tables

    def create_tables(self):
        for table_name in TABLES:
            table_description = TABLES[table_name]
            if self.does_tb_exist(table_name):
                print("the table {} already exists".format(table_name))
            else:
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
                              "id_categorie = {} "
                              "AND nom != '' "
                              "AND nutriscore != '' "
                              "LIMIT 12".format(category.id))
        self.cursor.execute(get_products_infos)
        for product in self.cursor:
            products.append(product)
        return products
