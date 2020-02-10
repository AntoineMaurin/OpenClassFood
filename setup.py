from database.database_setup import DatabaseSetup
from API.data_from_api import DataFromApi

setup = DatabaseSetup()
data = DataFromApi()

setup.connect('localhost', 'student', 'password')

setup.create_database('purbeurre')

data.request()
