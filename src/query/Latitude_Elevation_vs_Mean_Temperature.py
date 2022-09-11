## Latitude + Elevation vs Mean Temperature Query

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymongo
from numpy import NaN

db = pymongo.MongoClient("mongodb://gsod:1234@0.tcp.ap.ngrok.io:17088").gsod

df1 = pd.DataFrame([])

cols = db.weatherData

docs = cols.aggregate([
    {"$limit":1000000},
    {"$match": {"coordinate": {"$ne": NaN},"temperature":{"$ne":NaN},"elevation": {"$ne": NaN}}},
    {"$group":{
        "_id":  {"coordinate": "$station.location.coordinates",
                 "elevation":"$station.elevation"},
        "meanTemp": {"$avg": "$temperature"}
    }},
    {"$project":{ 
                "_id": 0,
                 "coordinate": "$_id.coordinate",
                 "elevation": "$_id.elevation",
                 "meanTemp": "$meanTemp"
    }},
])
df1 = pd.DataFrame(list(docs))
# display(df1)

coordinates = df1.iloc[:,0]
# display(coordinates)

latitudes = []

for i in range(len(coordinates)):
    latitude = coordinates[i]
    latitudes.append(latitude[1])
    
meanTemp = df1.iloc[:,-1]

elevations = df1.iloc[:,1]

## Plot Graph

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(x = latitudes, y = meanTemp)
plt.title("Mean Temperature vs Latitude")
plt.xlabel("Latitude (decimated degree)")
plt.ylabel("Mean Temperature (Fahrenheit)")


fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(x = elevations, y = meanTemp)
plt.title("Mean Temperature vs Elevation")
plt.xlabel("Elevation (metres)")
plt.ylabel("Mean Temperature (Fahrenheit)")
