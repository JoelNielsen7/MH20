import pymongo
import pandas as pd

def get_db():
    myclient = pymongo.MongoClient("mongodb+srv://SickoMode:SickoMode@cluster0-zfxxk.mongodb.net/test?retryWrites=true&w=majority")
    # db = myclient.test
    # print(db)
    # dblist = myclient.list_database_names()
    # print(dblist)
    mydb = myclient["SickoMode"]
    mycol = mydb["Diseases"]
    #
    #
    #mydict = { "gender": "M", "latitude": "44052343N","longitude" "diseases": [{'name': 'buttholeaids', 'percent': 80}, {'name': 'buttholeaids2', 'percent': 90}] }
    #
    #x = mycol.insert_one(mydict)


    x = mycol.find()

    keys = x[1].keys()

    dattylist = []
    keys = ["Latitude","Longitude", "Confirmed", "Diseases" ]
    for row in x:
        rowadd = [row["Latitude"], row["Longitude"], row["Confirmed"], row["Diseases"][0]["ID"], row["Diseases"][0]["Prob"], row["Diseases"][1]["ID"], row["Diseases"][1]["Prob"]]
        dattylist.append(rowadd)





    df = pd.DataFrame(dattylist, columns =['latitude', 'longitude', 'confirmed', 'd1_id', 'd1_prob', 'd2_id', 'd2_prob'], dtype = float)

    return(df)

