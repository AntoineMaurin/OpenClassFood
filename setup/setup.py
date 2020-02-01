import sys

sys.path.append('../database')

from database_setup import DatabaseSetup

setup = DatabaseSetup()

setup.connect('localhost', 'student', 'password')

setup.create_database('purbeurre')
