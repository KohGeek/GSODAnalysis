import pandas as pd

from gsodtools.getdb import get_db

db = get_db().gsod

df = pd.DataFrame([])

docs = db.weatherData.aggregate([
    {"$sort": {"gust": -1}},
    {"$limit": 20},
    {"$project": {
        "_id": 0,
        "Top 20 Highest Gust": "$gust",
        "Country": "$station.country.name",
        "Station": "$station.name"
    }}
])

df = pd.DataFrame(list(docs))
print(df)
