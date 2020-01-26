

#Collin Reinking
#collin.reinking@berkeley.edu

import folium

import pandas as pd
import re
import os
import branca.colormap as cm
import re
import numpy as np
from db import get_db


data = get_db()

hotshot = pd.get_dummies(data["d1_id"],data["d2_id"])
df = data[["latitude", "longitude", "d1_prob", "d2_prob"]]

df = df.join(hotshot, how='outer')

df

this_map = folium.Map(prefer_canvas=True)

def makeHref(url,link_text = None):
    if link_text == None:
        link_text = str(url)
    return '<a href="' + url + '"target="_blank">' + re.sub(r"[']+", "\\\\'", link_text[:45]) +'</a>'

def popopHTMLString(point):
    '''input: a series that contains a url somewhere in it and generate html'''
    html = 'Listing: ' + makeHref(point.confirmed, point.confirmed) + '<br>'
    html += 'Host: ' + makeHref(point.confirmed, point.confirmed)
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