from database.database_request import DatabaseRequest
from API.data_from_api import DataFromApi

setup = DatabaseRequest()
data = DataFromApi()

setup.create_tables()

# Receives data from API and adds it in database
data.request()
