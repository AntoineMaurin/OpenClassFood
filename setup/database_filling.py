import sys

sys.path.append("")

from database.database_populating import DatabasePopulating

pop = DatabasePopulating()

pop.data.request()

pop.populate()
