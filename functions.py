#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 22:23:38 2020

@author: viniciussaurin
"""

import base64
from math import radians, cos, sin, asin, sqrt
import folium as folium
from folium.plugins import HeatMap


def _repr_html_(self, **kwargs):
    html = base64.b64encode(self.render(**kwargs).encode('utf8')).decode('utf8')
    onload = (
        'this.contentDocument.open();'
        'this.contentDocument.write(atob(this.getAttribute(\'data-html\')));'
        'this.contentDocument.close();'
    )
    if self.height is None:
        iframe = (
            '<div style="width:{width};">'
            '<div style="position:relative;width:100%;height:0;padding-bottom:{ratio};">'
            '<iframe src="about:blank" style="position:absolute;width:100%;height:100%;left:0;top:0;'
            'border:none !important;" '
            'data-html={html} onload="{onload}" '
            'allowfullscreen webkitallowfullscreen mozallowfullscreen>'
            '</iframe>'
            '</div></div>').format
        iframe = iframe(html=html, onload=onload, width=self.width, ratio=self.ratio)
    else:
        iframe = ('<iframe src="about:blank" width="{width}" height="{height}"'
                  'style="border:none !important;" '
                  'data-html={html} onload="{onload}" '
                  '"allowfullscreen" "webkitallowfullscreen" "mozallowfullscreen">'
                  '</iframe>').format
        iframe = iframe(html=html, onload=onload, width=self.width, height=self.height)
    return iframe




def haversine(coordinates1, coordinates2):

    lon1 = coordinates1[1]
    lat1 = coordinates1[0]
    lon2 = coordinates2[1]
    lat2 = coordinates2[0]
    #Change to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    
    # Apply the harversine formula
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371
    return c * r


def uber_map(map_data, pois, period=None, semana=None):
    uber_map = dict()
    lat_lon = dict()
    
    for month in map_data.keys(): 
        map_data[month]["Weight"] = .1
        lat_lon[month] = map_data[month].query("Week_Day in @semana and Period == @period")[["Lat", "Lon", "Weight"]].values
        uber_map[month] = folium.Map(location=[40.7728, -74.0060], zoom_start=13)
        HeatMap(lat_lon[month], radius=10).add_to(uber_map[month])
        for poi in pois.items():
            folium.Marker((poi[1][0], poi[1][1]), popup="POI: {}".format(poi[0])).add_to(uber_map[month])
    return uber_map