import classes.console as console
from classes.db import DB
from classes.config import Config

# Set connection to the origin DB
config=Config()
db=DB(config.config_origin)
db.setConnection()
conn=db.getConnection()




# =======================
typeMigrate=console.askType()
typeParameters=console.askTypeParameters(typeMigrate)
if typeMigrate!="id":
    migrateIds=console.getMigrationIds(conn,typeMigrate,typeParameters)
else:
    migrateIds=typeParameters
# =======================


db.setLinkedTables(config.linked_tables)


db_dest=DB(config.config_destination)
db_dest.setConnection()
desrination_db=db_dest.getConnection()

if len(migrateIds)>0:
    db.migrate(desrination_db,migrateIds)
else:
    print("No appropriate items found!")

