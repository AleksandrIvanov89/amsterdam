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

places_df = pd.read_csv("fsq_places.csv")

# read foursquare API KEY

with open('../../credentials.json') as json_file:
    json_data = json.load(json_file)

headers = {"Accept": "application/json",
           "Authorization": json_data.get('API_KEY')}

url = "https://api.foursquare.com/v3/places/" + "4f6aeee9121d0c469321d38e" + "?fields=rating,popularity,price"
response = requests.request("GET", url, headers=headers)

print(response.json())
"""for place_i in places_df.iterrows():
    pass"""