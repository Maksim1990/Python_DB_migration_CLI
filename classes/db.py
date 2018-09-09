import pymysql
import datetime
from classes.file import File

class DB:

    def __init__(self, config):
        self.hostname=config['hostname']
        self.database=config['database']
        self.username=config['username']
        self.password=config['password']

    def getConnection(self):
        return self.connection

    def setConnection(self):
        self.connection = pymysql.connect( self.hostname, self.username, self.password, self.database )

    def setLinkedTables(self, tables):
        self.tables = tables

    def getLinkedTables(self):
        return self.tables

    def getTableFields(self, table ) :
        cur = self.getConnection().cursor()
        cur.execute("SHOW COLUMNS FROM {0}".format(table))
        # List of columns in the table
        columns=[]
        for item in cur.fetchall():
            columns.append(item[0])
        return columns

    def migrate(self,conn_destination,migrateIds):
        cur = self.getConnection().cursor()
        cur_dest = conn_destination.cursor()

        tables=self.getLinkedTables()
        for table in tables:

            # Get columns from the current table
            columns=self.getTableFields(table)
            str_columns=",".join(columns)


            strIds=", ".join(str(i) for i in migrateIds )
            strIds=strIds.strip(", ")

            if table != "users":
                columnName="user_id"
            else:
                columnName="id"

            cur.execute("SELECT {} FROM {} WHERE {} IN ({})".format(str_columns,table,columnName,strIds))
            data=cur.fetchall()

            # Check if migrated data list from current table is not empty
            if data:
                for line in data:
                    i=0
                    strValues=""
                    status=True
                    # Build string for parameters to be replaced in SQL query
                    while i<len(line):
                        strValues+="%s"
                        if i!= (len(line)-1):
                            strValues+=","
                        i+=1
                    try:
                        cur_dest.execute(" INSERT INTO {} ({}) VALUES ({}) ".format(table,str_columns,strValues), (line))
                        conn_destination.commit()
                    except:
                        status=False
                        file=File("logging.txt")
                        file.log("[{}] WARNING! Entry with id {} already exist in {} table \n".format(datetime.datetime.now(),line[0],table))
            else:
                print("Table has no relevant data to migrate")

        conn_destination.close()
        print("\nMigration completed!")

        if not status:
                print("\nDetected duplicates in destination DB")
                print("For more details refer to log file: {}".format("storage/logging.txt"))
        else:
            file=File("logging.txt")
            file.log("[{}] SUCCESS! Migration successfully completed! \n".format(datetime.datetime.now()))


