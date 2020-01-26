import pymongo
def most_common(lst):
    return max(set(lst), key=lst.count)
#Collin Reinking
#collin.reinking@berkeley.edu
from statistics import mean
from statistics import stdev
import folium
from sklearn.cluster import DBSCAN
import pandas as pd
import re
import os
import branca.colormap as cm
import re
import numpy as np
import datetime
from db import get_db_two
from db import get_db
import time
from sklearn.preprocessing import StandardScaler
def get_curdata():
    data = get_db()

    hotshot = pd.get_dummies(data["d1_id"],data["d2_id"])
    df = data[["latitude", "longitude", "d1_prob", "d2_prob"]]
    dfscaled = pd.DataFrame(StandardScaler().fit_transform(df))

    scaled_joined = df.join(hotshot, how='outer')



    db = DBSCAN(eps=.7, min_samples=3).fit(scaled_joined)
    labels = db.labels_


    scaled_joined = df.join(pd.DataFrame(labels), how='outer')

    col = scaled_joined.columns


    data = scaled_joined[["latitude", "longitude", 0]]

    data.columns =  ["latituude", "longituude", "type"]


    og = get_db()
    ogplus = pd.concat([og, data], axis = 1)

    magic_dic = {}
    for index, row in ogplus.iterrows():
        if row["type"] not in magic_dic.keys():
            magic_dic[row["type"]] = [[], [], []]
        magic_dic[row["type"]][0].append(row["latitude"])
        magic_dic[row["type"]][1].append(row["longitude"])
        magic_dic[row["type"]][2].append(row["d1_id"])

    magic_list = []

    for key in magic_dic.keys():
        if key != -1:
            magic_list.append(
                [mean(magic_dic[key][0]),mean(magic_dic[key][1]),stdev(magic_dic[key][1]), most_common(magic_dic[key][2]), magic_dic[key][2].count(most_common(magic_dic[key][2]))])

    data = pd.DataFrame(magic_list, columns =['latitude', 'longitude', 'stddev', "name", "count"], dtype = float)
    return data
def update_dots():
    data = get_curdata()
    myclient = pymongo.MongoClient(
        "mongodb+srv://SickoMode:SickoMode@cluster0-zfxxk.mongodb.net/test?retryWrites=true&w=majority")
    # db = myclient.test
    # print(db)
    # dblist = myclient.list_database_names()
    # print(dblist)
    mydb = myclient["SickoMode"]
    mycol = mydb["dots"]

    counter = 0
    listadd = []
    for number in range(0,15):
        counter += 1
        for index, row in data.iterrows():
            number = 1 + number/4
            day_delta = counter
            if index ==0:
                mydict = {"latitude": row["latitude"]+.0029*number, "longitude": row["longitude"]-.0019*number, "id": row["name"], "std": row["stddev"]/(1.16+number*1.1), "date": datetime.datetime.now()- datetime.timedelta(days=day_delta, hours=3), "number": 2}
            if index == 1:
                mydict = {"latitude": row["latitude"]-.008*number, "longitude": row["longitude"]+.001*number, "id": row["name"],
                          "std": row["stddev"] / (1.16+number), "date": datetime.datetime.now() - datetime.timedelta(days=day_delta, hours=3),
                          "number": 2}
            if index == 2:
                mydict = {"latitude": row["latitude"]+.0026*number, "longitude": row["longitude"]-.0011*number, "id": row["name"],
                          "std": row["stddev"] / (1.16+number*2), "date": datetime.datetime.now() - datetime.timedelta(days=day_delta, hours=3),
                          "number": 2}
                print("here")

            if index == 3:
                mydict = {"latitude": row["latitude"], "longitude": row["longitude"]+.263*number, "id": row["name"],
                          "std": row["stddev"] / (1.16+number), "date": datetime.datetime.now() - datetime.timedelta(days=day_delta, hours=3),
                          "number": 2}

            if index == 4:
                mydict = {"latitude": row["latitude"], "longitude": row["longitude"], "id": row["name"],
                          "std": row["stddev"] /(1.16+number*1.1), "date": datetime.datetime.now() - datetime.timedelta(days=day_delta, hours=3),
                          "number": 2}
                print("here")
            if index == 5:
                mydict = {"latitude": row["latitude"], "longitude": row["longitude"], "id": row["name"],
                          "std": row["stddev"] / 2.1, "date": datetime.datetime.now() - datetime.timedelta(days=day_delta, hours=3),
                          "number": 2}
                print("here")

            time.sleep(.1)
            mycol.insert_one(mydict)





def get_html(data):
    this_map = folium.Map(prefer_canvas=True)
    folium.TileLayer('cartodbpositron').add_to(this_map)

    def makeHref(url,link_text = None):
        if link_text == None:
            link_text = str(url)
        return '<a href="' + url + '"target="_blank">' + re.sub(r"[']+", "\\\\'", link_text[:45]) +'</a>'

    def popopHTMLString(point):
        '''input: a series that contains a url somewhere in it and generate html'''
        html = 'Listing: ' + makeHref("adsf", "buttwhole aids") + '<br>'
        html += 'Host: ' + makeHref("hey", "15 people died")
        return html

    def plotDot(point):
        '''input: series that contains a numeric named latitude and a numeric named longitude
        this function creates a CircleMarker and adds it to your this_map'''
        htmlString = folium.Html(popopHTMLString(point), script=True)
        list = [ "#660033", "#336600", "#000066"]


        folium.CircleMarker(location=[point.latitude, point.longitude],
                            radius=19*point.stddev*150,
                            weight=1,#remove outline
                            popup = folium.Popup(htmlString),
                            fill_color=list[1]).add_to(this_map)

    #use df.apply(,axis=1) to iterate through every row in your dataframe
    data.apply(plotDot, axis = 1)

    #Set the zoom to the maximum possible
    this_map.fit_bounds(this_map.get_bounds())

    #Save the map to an HTML file
    #this_map.save(os.path.join('html_map_output/html_pop_up.html'))


    this_map.save("templates/hello.html")
    
    phrase1 = '<head>'
    phrase2 = '<body>'
    html1 = ''' <link href="{{ url_for('static', filename='css/home_style.css') }}" rel="stylesheet"> '''
    html2 = ''' <nav>
      <ul class="nav">
        <li><a href=./>Home</a></li>
        <li><a href=./form.html>Submit Symptoms</a></li>
        <li><a href=./about.html>About</a></li>
      </ul>
    </nav>
'''
    found1 = False
    found2 = False
    with open('templates/hello.html') as f:
        file = f.read()
        i1 = file.index(phrase1)
        i1 += 7
        file = file[:i1] + html1 + file[i1:]
        i2 = file.index(phrase2)
        i2 += 7
        file = file[:i2] + html2 + file[i2:]

    fp = open('./templates/hello.html', 'w')
    fp.write(file)
    fp.close()

    return this_map
