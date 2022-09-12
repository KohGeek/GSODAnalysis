import pandas as pd
from numpy import NaN

from src.tools.getdb import get_db

db = get_db().gsod

df = pd.DataFrame([])

docs = db.weatherData.aggregate([
    {"$sort": {"precipitation": -1}},
    {"$limit": 20},
    {"$project": {
        "_id": 0,
        "Top 20 Highest Precipitation": "$precipitation",
        "Country": "$station.country.name",
        "Station": "$station.name"
    }}
])

df = pd.DataFrame(list(docs))
print(df)
