import sys

sys.path.append("")

from database.database_setup import DatabaseSetup

setup = DatabaseSetup()

setup.connect('localhost', 'student', 'password')

setup.create_database('purbeurre')
