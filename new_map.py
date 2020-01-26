import folium

from pathlib import Path
import pandas as pd
import numpy as np

import seaborn as sns
import folium
from folium.plugins import TimestampedGeoJson
from diseases import build_disease_map

from db import get_db_two
def create_geojson_features(df):
    features = []
    map = build_disease_map()
    x = 0
    color = ["#8FC6B4","#BAC39F","#E5B374","#F99D78","#829C9C", "#E4C678", "#D25A43", "#3C7769", "#26AA4A", "#D88284", "#D9D83C", "#22C941", "#354B66", "#75CDC6"]
    disList = []
    for _, row in df.iterrows():

        dis = map[row["id"]]
        if dis in disList:
            pass
        else:
            disList.append(dis)

        feature = {
            'type': 'Feature',
            'geometry': {
                'type':'Point',
                'coordinates':[row['longitude'],row['latitude']]
            },
            'properties': {
                'time': row['std'].date().__str__(),
                'style': {'color' : color[disList.index(dis)]},
                'icon': 'circle',
                'popup': " <b>Warning: " + str(row['date']) + " cases of <u>" + dis +"</u> reported in this area. </b <br><a href = https://www.webmd.com/search/search_results/default.aspx?query="+ dis.replace(" ",'_') +"> Learn more here </a>",
                'iconstyle':{
                    'fillColor': color[disList.index(dis)],
                    'fillOpacity': .6,
                    'stroke': 'False',
                    'radius': (1000 * float(row['name']))
                }
            }
        }

        features.append(feature)
    return features

def make_map(features):
    coords=[44.958057, -93.265234]
    this_map = folium.Map(location=coords, control_scale=True, zoom_start=11)
    folium.TileLayer('cartodbpositron').add_to(this_map)

    temp = TimestampedGeoJson(
        {'type': 'FeatureCollection',
        'features': features}
        , period='P1M'
        , add_last_point=True
        , auto_play=True
        , loop=True
        , max_speed=.7
        , loop_button=True
        , date_options='YYYY/MM'
        , time_slider_drag_update=True
    )

    temp.add_to(this_map)
    this_map.save("templates/hello.html")
    phrase1 = '<head>'
    phrase2 = '<body>'
    html1 = ''' <link href="{{ url_for('static', filename='css/home_style.css') }}" rel="stylesheet"> '''
    html2 = ''' <nav>
      <ul class="bar nav">
        <li class="bar"><a href=./ class="active_bar bar">Home</a></li>
        <li class="bar"><a href=./form class="bar">Submit Symptoms</a></li>
        <li class="bar"><a href=./about class="bar">About</a></li>
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

    print("Yeet:", file)
    return this_map

#data = get_db_two()
#features = create_geojson_features(data)
#map = make_map(features)


#map.save("hello.html")
