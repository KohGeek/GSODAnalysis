## Mean Temp vs Snow Depth Query

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
    {"$match": {"snowDepth": {"$ne": NaN},"temperature":{"$ne":NaN}}},
    {"$group":{
        "_id":  {"snowDepth":{"$avg": "$snowDepth"}},
        "meanTemp": {"$avg": "$temperature"}
    }},
    {"$project":{ 
                "_id": 0,
                 "snowDepth": "$_id.snowDepth",
                 "meanTemp": "$meanTemp"
    }},
])

df1 = pd.DataFrame(list(docs))
# display(df1)

meanSnowDepth = df1.iloc[:,0]
# display(snowDepth)

meanTemp = df1.iloc[:,-1]

## Plot Graph

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(x = meanTemp, y = meanSnowDepth)
plt.title("Mean Snow Depth vs Mean Temperature")
plt.xlabel("Mean Temperature (Fahrenheit)")
plt.ylabel("Mean Snow Depth (inches)")
