import pandas as pd
import pymongo
from numpy import NaN


db = pymongo.MongoClient("mongodb://gsod:1234@0.tcp.ap.ngrok.io:17088").gsod

df = pd.DataFrame([])

docs = db.weatherData.aggregate([
    {"$match": {"temperature": {"$ne": NaN}}},
    {"$sort": {"temperature": -1}},
    {"$limit": 20},
    {"$project": {
        "_id": 0,
        "Top 20 Highest Temperature": "$temperature",
        "Country": "$station.country.name",
        "Station": "$station.name"
    }}
])

df = pd.DataFrame(list(docs))
print(df)
