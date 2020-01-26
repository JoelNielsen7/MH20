

#Collin Reinking
#collin.reinking@berkeley.edu

import folium

import pandas as pd
import re
import os
import branca.colormap as cm
import re
import numpy as np


import pymongo
import pandas as pd
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


data = df



this_map = folium.Map(prefer_canvas=True)

def makeHref(url,link_text = None):
    if link_text == None:
        link_text = str(url)
    return '<a href="' + url + '"target="_blank">' + re.sub(r"[']+", "\\\\'", link_text[:45]) +'</a>'

def popopHTMLString(point):
    '''input: a series that contains a url somewhere in it and generate html'''
    html = 'Listing: ' + makeHref(point.d1_prob, point.d1_id) + '<br>'
    html += 'Host: ' + makeHref(point.d2_id, point.d2_id)
    return html

def plotDot(point):
    '''input: series that contains a numeric named latitude and a numeric named longitude
    this function creates a CircleMarker and adds it to your this_map'''
    htmlString = folium.Html(popopHTMLString(point), script=True)
    folium.CircleMarker(location=[point.latitude, point.longitude],
                        radius=9,
                        weight=0,#remove outline
                        popup = folium.Popup(htmlString),
                        fill_color='#000000').add_to(this_map)

#use df.apply(,axis=1) to iterate through every row in your dataframe
data.apply(plotDot, axis = 1)

#Set the zoom to the maximum possible
this_map.fit_bounds(this_map.get_bounds())

#Save the map to an HTML file
#this_map.save(os.path.join('html_map_output/html_pop_up.html'))


this_map.save("hello.html")