import pandas as pd
import numpy as np
import geopandas as gpd
from geopy.geocoders import Nominatim
from geopy.distance import distance
from shapely.geometry import Point
import json
import re
import requests
import math
import time

# load boroughs geodata
boroughs_geodata_filepath = '../amsterdam.nl/districts-geojson_lnglat.json'
print('Boroughs geodata loadfing from file: {}'.format(boroughs_geodata_filepath))
boroughs_geodata = gpd.read_file(boroughs_geodata_filepath)
print("Boroughs geodata loaded")

# amsterdam boundaries
amsterdam_bounds = [500, 500, 0, 0]

for borough_i in boroughs_geodata.iterrows():
    for i in range(4):
        amsterdam_bounds[i] = min(amsterdam_bounds[i], borough_i[1].geometry.bounds[i]) if i < 2 else max(amsterdam_bounds[i], borough_i[1].geometry.bounds[i])

print(amsterdam_bounds)

# calculation of steps in boundaries

address  = 'Amsterdam, Netherlands'
geolocator = Nominatim(user_agent="Amsterdam Data Project")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('{} : Latitude: {}, Longitude: {}.'.format(address, latitude, longitude))

radius = 500.0

dst = radius * 2.0 * math.sqrt(2.0)

step_lat_1 = latitude * 0.0001
dst_1 = distance((latitude, longitude), (latitude + step_lat_1, longitude)).m
step_lat = dst * step_lat_1 / dst_1

step_lng_1 = longitude * 0.0001
dst_1 = distance((latitude, longitude), (latitude, longitude + step_lng_1)).m
step_lng = dst * step_lng_1 / dst_1

# generate the list of points within amsterdam

points = []
for x in range(int((amsterdam_bounds[2] - amsterdam_bounds[0]) / step_lng + 1)):
    for y in range(int((amsterdam_bounds[3] - amsterdam_bounds[1]) / step_lat + 1)):
        point_i = Point(amsterdam_bounds[0] + x * step_lng, amsterdam_bounds[1] + y * step_lat)
        temp = False
        for borough_i in boroughs_geodata.iterrows():
            temp = point_i.within(borough_i[1].geometry) or temp
        if temp:
            points.append(point_i)

# read foursquare API KEY

with open('../../credentials.json') as json_file:
    json_data = json.load(json_file)

# foursquare requests

LIMIT = 50

url = 'https://api.foursquare.com/v3/places/search?&ll={},{}&radius={}&limit={}'.format(
    points[50].y, 
    points[50].x, 
    radius, 
    LIMIT)

headers = {"Accept": "application/json", "Authorization": json_data.get('API_KEY')}
response = requests.request("GET", url, headers=headers)

#results = requests.get(url).json()#["response"]#['groups'][0]['items']
print(json.dumps(response.json(), indent=2))
print(len(response.json()["results"]))
