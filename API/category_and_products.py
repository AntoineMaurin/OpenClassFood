class Product:
    def __init__(self, name, description, nutriscore, stores, url):
        self.name = name
        self.description = description
        self.nutriscore = nutriscore
        self.stores = stores
        self.url = url
        self.category = ""

class Category:
    def __init__(self, name):
        self.name = name
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def get_products(self):
        return self.products
