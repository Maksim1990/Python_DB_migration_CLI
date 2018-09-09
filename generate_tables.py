import classes.console as console
from classes.db import DB
from config.config import Config

# Set connection to the origin DB
config=Config()
db=DB(config.config_origin)
db.setConnection()
db.setLinkedTables(config.linked_tables)


db_dest=DB(config.config_destination)
db_dest.setConnection()
desrination_db=db_dest.getConnection()


db.generateTables(desrination_db)

