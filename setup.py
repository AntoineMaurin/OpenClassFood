from database.database_setup import DatabaseSetup
from API.data_from_api import DataFromApi

# Creation of instances of the two imported classes
setup = DatabaseSetup()
data = DataFromApi()

# Connexion to database with requested parameters
setup.connect('localhost', 'student', 'password')

# Creation of the database with the name in parameter
setup.create_database('purbeurre')

# Data receiving from API and adding in database
data.request()
