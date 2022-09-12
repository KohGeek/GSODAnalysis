# Mean Temp vs Snow Depth Query

import pandas as pd
import matplotlib.pyplot as plt
from numpy import NaN

from src.tools.getdb import get_db

db = get_db().gsod

df1 = pd.DataFrame([])

cols = db.weatherData

docs = cols.aggregate([
    {"$limit": 1000000},
    {"$group": {
        "_id":  {"snowDepth": {"$avg": "$snowDepth"}},
        "meanTemp": {"$avg": "$temperature"}
    }},
    {"$project": {
        "_id": 0,
        "snowDepth": "$_id.snowDepth",
        "meanTemp": "$meanTemp"
    }},
])

df1 = pd.DataFrame(list(docs))
# display(df1)

meanSnowDepth = df1.iloc[:, 0]
# display(snowDepth)

meanTemp = df1.iloc[:, -1]

# Plot Graph

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(x=meanTemp, y=meanSnowDepth)
plt.title("Mean Snow Depth vs Mean Temperature")
plt.xlabel("Mean Temperature (Fahrenheit)")
plt.ylabel("Mean Snow Depth (inches)")

plt.show()
