import pymongo

myclient = pymongo.MongoClient("mongodb+srv://SickoMode:SickoMode@cluster0-zfxxk.mongodb.net/test?retryWrites=true&w=majority")
# db = myclient.test
# print(db)
# dblist = myclient.list_database_names()
# print(dblist)
mydb = myclient["SickoMode"]
mycol = mydb["Diseases"]
#
#
mydict = { "gender": "M", "latitude": "44052343N", "diseases": [{'name': 'buttholeaids', 'percent': 80}, {'name': 'buttholeaids2', 'percent': 90}] }
#
x = mycol.insert_one(mydict)
#
print(x.inserted_id)
#
