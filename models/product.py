from database.database_setup import DatabaseSetup

class Product:
    def __init__(self, name, description, nutriscore, stores, url, category):
        self.name = name
        self.description = description
        self.nutriscore = nutriscore
        self.stores = stores
        self.url = url
        self.category = category
        self.id = ""

    def connect_to_db(self):
        self.dbsetup = DatabaseSetup()
        self.dbsetup.connect('localhost', 'student', 'password')
        self.dbsetup.use_db('purbeurre')

    def get_substitute(cls, category_id):
        cls.connect_to_db()
        get_substitute_infos = ("SELECT id, nom, description, nutriscore,"
                                "magasin, lien_openfoodfacts, id_categorie "
                                "FROM aliment WHERE "
                                "id_categorie = {} "
                                "AND nom != '' "
                                "AND nutriscore != '' "
                                "ORDER BY nutriscore "
                                "LIMIT 1".format(category_id))
        cls.dbsetup.cursor.execute(get_substitute_infos)

        for id, name, desc, ntsc, store, url_off, cat_id in cls.dbsetup.cursor:
            substitute_name = name
            substitute_description = desc
            substitute_nutriscore = ntsc
            substitute_store = store
            substitute_url = url_off
            substitute_category = cat_id

            substitute = Product(substitute_name, substitute_description,
                                 substitute_nutriscore, substitute_store, 
                                 substitute_url, substitute_category)
            substitute.id = id
        return substitute
