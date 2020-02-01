import sys

sys.path.append('../database')

from database_populating import DatabasePopulating

pop = DatabasePopulating()

pop.data.request()

pop.populate()
