import pymongo
import pandas as pd

from sklearn.preprocessing import OneHotEncoder

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



    dattylist = []
    for row in x:
        if len(row["Diseases"]) > 1:
            if row["Confirmed"] != "y":
                rowadd = [row["Latitude"], row["Longitude"], row["Confirmed"], int(row["Diseases"][0]["ID"]),
                          row["Diseases"][0]["Prob"]/100, int(row["Diseases"][1]["ID"]), row["Diseases"][1]["Prob"]/100, row["Date"]]
            else:
                rowadd = [row["Latitude"], row["Longitude"], row["Confirmed"], int(row["Diseases"][0]["ID"]),
                          1, int(row["Diseases"][1]["ID"]), 0, row["Date"]]

            dattylist.append(rowadd)

    df = pd.DataFrame(dattylist, columns =['latitude', 'longitude', 'confirmed', 'd1_id', 'd1_prob', 'd2_id', 'd2_prob',"Date"], dtype = int)


    return(df)

