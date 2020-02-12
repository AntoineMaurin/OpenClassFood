from database.database_request import DatabaseRequest
from API.data_from_api import DataFromApi

# Creation of instances of the two imported classes
setup = DatabaseRequest()
data = DataFromApi()

# Creation of the database with the name in parameter
setup.create_database('purbeurre')

# Data receiving from API and adding in database
data.request()
