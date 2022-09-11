# Mean Sea Level Pressure vs Mean Wind Speed Query

import pandas as pd
import matplotlib.pyplot as plt
import pymongo
from numpy import NaN

db = pymongo.MongoClient("mongodb://gsod:1234@0.tcp.ap.ngrok.io:17088").gsod

df1 = pd.DataFrame([])

cols = db.weatherData

docs = cols.aggregate([
    {"$limit": 1000000},
    {"$match": {"seaLevelPressure": {"$ne": NaN}, "windSpeed": {"$ne": NaN}}},
    {"$group": {
        "_id":  {"meanWS": {"$avg": "$windSpeed"}},
        "meanSTP": {"$avg": "$seaLevelPressure"},

    }},
    {"$project": {
        "_id": 0,
        "meanSTP": "$meanSTP",
        "meanWS": "$_id.meanWS"
    }},
])

df1 = pd.DataFrame(list(docs))
# display(df1)

meanSeaLevelPressures = df1.iloc[:, 0]
# display(snowDepth)

meanWindSpeeds = df1.iloc[:, 1]

# Plot Graph

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(x=meanSeaLevelPressures, y=meanWindSpeeds)
plt.title("Mean Wind Speed vs Mean Sea Level Pressure")
plt.xlabel("Mean Sea Level Pressure (in millibars to tenths)")
plt.ylabel("Mean Wind Speed (in knots to tenths)")

plt.show()
