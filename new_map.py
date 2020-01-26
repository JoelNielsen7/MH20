import folium

from pathlib import Path
import pandas as pd
import numpy as np

import seaborn as sns
import folium
from folium.plugins import TimestampedGeoJson

from db import get_db_two
def create_geojson_features(df):
    print('> Creating GeoJSON features...')
    features = []
    for _, row in df.iterrows():
        feature = {
            'type': 'Feature',
            'geometry': {
                'type':'Point',
                'coordinates':[row['longitude'],row['latitude']]
            },
            'properties': {
                'time': row['std'].date().__str__(),
                'style': {'color' : "#000066"},
                'icon': 'circle',
                'iconstyle':{
                    'fillColor': "#000066",
                    'fillOpacity': 1,
                    'stroke': 'true',
                    'radius': 1000
                }
            }
        }
        features.append(feature)
    return features

def make_map(features):
    print('> Making map...')
    coords_belgium=[50.5039, 4.4699]
    pollution_map = folium.Map(location=coords_belgium, control_scale=True, zoom_start=8)

    TimestampedGeoJson(
        {'type': 'FeatureCollection',
        'features': features}
        , period='P1M'
        , add_last_point=True
        , auto_play=False
        , loop=False
        , max_speed=1
        , loop_button=True
        , date_options='YYYY/MM'
        , time_slider_drag_update=True
    ).add_to(pollution_map)
    print('> Done.')
    return pollution_map

data = get_db_two()
features = create_geojson_features(data)
map = make_map(features)
map.save("hello.html")