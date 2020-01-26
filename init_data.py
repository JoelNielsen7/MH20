# generate random Gaussian values
from random import seed
from random import gauss
from random import random

import pymongo

import datetime
# seed random number generator
seed(1)


myclient = pymongo.MongoClient("mongodb+srv://SickoMode:SickoMode@cluster0-zfxxk.mongodb.net/test?retryWrites=true&w=majority")

"""
flu = {
    "Diseases": [
        {"Name":"Flu","Prob":81.5},
        {"Name":"Cold","Prob":58}
    ]
}
"""
flu = {
    "Diseases": [
        {"ID":11,"Prob":81.5},
        {"ID":80,"Prob":58}
    ]
}

flu_center = [44.974331, -93.227279]
flu_radius = 0.02

"""
food = {
    "Diseases": [
        {"Name":"Food poisoning","Prob":71.8},
        {"Name":"Poisoning","Prob":47.123}
    ]
}
"""

food = {
    "Diseases": [
        {"ID":281,"Prob":71.8},
        {"ID":443,"Prob":47.123}
    ]
}

food_center = [44.949251, -93.234097]
food_radius = 0.005

"""
pink = {
    "Diseases": [
        {"Name":"Pink eye","Prob":89},
        {"Name":"Cold","Prob":55}
    ]
}
"""

pink = {
    "Diseases": [
        {"ID":140,"Prob":89},
        {"ID":80,"Prob":55}
    ]
}

pink_center = [44.920959, -93.466897]
pink_radius = 0.08


init_data = []

# Flu
for i in range(35):
    x = gauss(0,flu_radius)
    y = gauss(0,flu_radius)
    gender = 'male'
    if(i % 2 == 0):
        gender = 'female'
    loc = [flu_center[0] + x, flu_center[1] + y]
    age = int(gauss(21,2))
    conf = random()
    confirmed = 'n'

    if(conf < 0.05):
        confirmed = 'y'

    new_report = {
        "Gender": gender,
        "Latitude": loc[0],
        "Longitude": loc[1],
        "Age": age,
        "Symptoms": [],
        "Confirmed": confirmed,
        "Date": "2020-01-25 21:59:18.197503",
        "Diseases": flu["Diseases"]
    }

    init_data.append(new_report)


# Food poisoning
for i in range(5):
    x = gauss(0,food_radius)
    y = gauss(0,food_radius)
    gender = 'male'
    if(i % 2 == 0):
        gender = 'female'
    loc = [food_center[0] + x, food_center[1] + y]
    age = int(gauss(30,6))
    conf = random()
    confirmed = 'n'

    if(conf < 0.15):
        confirmed = 'y'

    new_report = {
        "Gender": gender,
        "Latitude": loc[0],
        "Longitude": loc[1],
        "Age": age,
        "Symptoms": [],
        "Confirmed": confirmed,
        "Date": "2020-01-25 21:59:18.197503",
        "Diseases": food["Diseases"]
    }

    init_data.append(new_report)

# Pink eye
for i in range(20):
    x = gauss(0,pink_radius)
    y = gauss(0,pink_radius)
    gender = 'male'
    if(i % 2 == 0):
        gender = 'female'
    loc = [pink_center[0] + x, pink_center[1] + y]
    age = int(gauss(15,3))
    conf = random()
    confirmed = 'n'

    if(conf < 0.60):
        confirmed = 'y'

    new_report = {
        "Gender": gender,
        "Latitude": loc[0],
        "Longitude": loc[1],
        "Age": age,
        "Symptoms": [],
        "Confirmed": confirmed,
        "Date": "2020-01-25 21:59:18.197503",
        "Diseases": pink["Diseases"]
    }

    init_data.append(new_report)

mydb = myclient["SickoMode"]
mycol = mydb["Diseases"]

# mycol.drop()

x = mycol.insert_many(init_data)
#

#print(init_data)
