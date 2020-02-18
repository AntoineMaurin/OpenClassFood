from database.database_request import DatabaseRequest


class Product:
    def __init__(self, name, description, nutriscore, stores, url, category):
        self.id = ""
        self.name = name
        self.description = description
        self.nutriscore = nutriscore
        self.stores = stores
        self.url = url
        self.category = category

    def get_substitute(self):
        self.db_rq = DatabaseRequest()
        result = self.db_rq.get_substitute(self)
        substitute_name = result[1]
        substitute_description = result[2]
        substitute_nutriscore = result[3]
        substitute_store = result[4]
        substitute_url = result[5]
        substitute_category_id = result[6]
        substitute = Product(substitute_name, substitute_description,
                             substitute_nutriscore, substitute_store,
                             substitute_url, substitute_category_id)
        substitute.id = result[0]
        return substitute
