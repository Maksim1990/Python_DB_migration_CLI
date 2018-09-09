import datetime

def askType():
    typeMigrate=input("Choose type ([id,time,name]) [id]")
    allowedType=("id","time","name")
    if typeMigrate:
        if typeMigrate.lower() not in allowedType:
            typeMigrate=askType()
    else:
        typeMigrate="id"
    return typeMigrate.lower()

def askTypeParameters(type):

    allowedType=("id","time","name")
    if type =="id":
        param=input("Type comma separated IDs [1,2,3,10]")
        param=param.split(",")
    elif type =="name":
        param=input("Type name of user to be found (similar names will be found)")
    elif type =="time":
        param=input("Type date period with following format [before yy-m-d, after yy-md]")

    if param=="":
           param=askTypeParameters(type)
    return param

def getMigrationIds(conn,type, params):
    cur = conn.cursor()
    blnMigrateStatus=True
    if type == "name":
        strQuery="SELECT id,name FROM users WHERE name LIKE '%{}%'".format(params)
        cur.execute(strQuery)
    if type == "time":

        if "before" in params:
            dateCompareSign="<"
        elif "after" in params:
            dateCompareSign=">"
        else:
            blnMigrateStatus=False
            print("Invalid time format")

        if blnMigrateStatus:
            dateParam=params.split(" ")
            listDateParams=dateParam[1].split("-")
            strDateTime = datetime.datetime(int(listDateParams[0]),int(listDateParams[1]),int(listDateParams[2]))
            strQuery="SELECT id,name FROM users WHERE DATE(created_at) {0} '{1}'".format(dateCompareSign,strDateTime)
            cur.execute(strQuery)

    migrateIds=[]

    if blnMigrateStatus:
        data=cur.fetchall()

        if data:
            for id,name in data:
                migrateIds.append(id)

    return migrateIds
