# Latitude + Elevation vs Mean Temperature Query

import pandas as pd
import matplotlib.pyplot as plt

from src.tools.getdb import get_db

db = get_db().gsod

df1 = pd.DataFrame([])

cols = db.weatherData

docs = cols.aggregate([
    {"$limit": 1000000},
    {"$group": {
        "_id":  {"coordinate": "$station.location.coordinates",
                 "elevation": "$station.elevation"},
        "meanTemp": {"$avg": "$temperature"}
    }},
    {"$project": {
        "_id": 0,
        "coordinate": "$_id.coordinate",
        "elevation": "$_id.elevation",
        "meanTemp": "$meanTemp"
    }},
])

df1 = pd.DataFrame(list(docs))
# display(df1)

coordinates = df1.iloc[:, 0]
# display(coordinates)

latitudes = []

for i, row in enumerate(coordinates):
    latitude = row
    latitudes.append(latitude[1])

meanTemp = df1.iloc[:, -1]
elevations = df1.iloc[:, 1]

# Plot Graph

fig, ax = plt.subplots(figsize=(10, 6))
plt.xlabel("Latitude (decimated degree)")
plt.ylabel("Mean Temperature (Fahrenheit)")
ax.scatter(x=latitudes, y=meanTemp)
plt.title("Mean Temperature vs Latitude")

plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
plt.xlabel("Latitude (decimated degree)")
plt.ylabel("Mean Temperature (Fahrenheit)")
ax.scatter(x=elevations, y=meanTemp)
plt.title("Mean Temperature vs Elevation")

plt.show()
