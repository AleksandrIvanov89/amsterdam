import pandas as pd
import numpy as np
import json
import re
import requests
import math
import time
from os.path import exists

# read input file

input_file = "fsq_places.csv"

places_df = pd.DataFrame(columns=['id', 'name', 'categories', 'latitude', 'longitude'])

if (exists(input_file)):
    places_df = pd.read_csv(input_file)

# read output file with already loaded data or create new one

output_file = "fsq_data.csv"

if (exists(output_file)):
    fsq_df = pd.read_csv(output_file)
    fsq_df = fsq_df[['id', 'name', 'categories', 'latitude', 'longitude', 'rating', 'popularity', 'price']]
    print(fsq_df)
else:
    fsq_df = pd.DataFrame(columns = ['id', 'name', 'categories', 'latitude', 'longitude', 'rating', 'popularity', 'price'])

# read foursquare API KEY

with open('../../credentials.json') as json_file:
    json_data = json.load(json_file)

# headers for requests

headers = {"Accept": "application/json",
           "Authorization": json_data.get('API_KEY')}

for place_i in places_df.iterrows():
    print(place_i[1]['id'])
    # check if is already collected
    if (not (place_i[1]['id'] in fsq_df['id'].values)):
        # prepare url
        url = "https://api.foursquare.com/v3/places/" + place_i[1].id + "?fields=rating,popularity,price"
        try:
            # request data
            response = requests.request("GET", url, headers=headers)
            # parsing response
            rating = response.json()['rating'] if 'rating' in response.json() else np.nan
            popularity = response.json()['popularity'] if 'popularity' in response.json() else np.nan
            price = response.json()['price'] if 'price' in response.json() else np.nan
            # add to dataFrame
            fsq_df = fsq_df.append({
                'id': place_i[1]['id'],
                'name': place_i[1]['name'],
                'categories': place_i[1]['categories'],
                'latitude': place_i[1]['latitude'],
                'longitude': place_i[1]['longitude'],
                'rating': rating,
                'popularity': popularity,
                'price': price
            }, ignore_index=True)
            print(fsq_df)
            # save to file
            fsq_df.to_csv(output_file)
        except Exception as e:
            print(e.args)
        # wait between responses to be in a free usage limit
        time.sleep(100)