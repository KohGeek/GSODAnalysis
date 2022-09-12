# Relative Humidity (100(EXP((17.625TD)/(243.04+TD))/EXP((17.625*T)/(243.04+T)))) vs visibility Query

import math
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
        "_id":  {"meanVisibility": {"$avg": "$visibility"}, },
        "meanTemp": {"$avg": "$temperature"},
        "meanDew": {"$avg": "$dewPoint"},
    }},
    {"$project": {
        "_id": 0,
        "meanDew": "$meanDew",
        "meanTemp": "$meanTemp",
        "meanVisibility": "$_id.meanVisibility",
    }},
])

df1 = pd.DataFrame(list(docs))
# display(df1)

meanDews = df1.iloc[:, 0]
meanTemp = df1.iloc[:, 1]
meanVisibilities = df1.iloc[:, 2]

# Calculating relative humidity
relativeHumidities = []

for i in range(len(df1)):
    relativeHumidity = 100*(math.exp((17.625*meanDews[i])/(243.04+meanDews[i]))
                            / math.exp((17.625*meanTemp[i])/(243.04+meanTemp[i])))
    relativeHumidities.append(relativeHumidity)


# Plot Graph

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(x=relativeHumidities, y=meanVisibilities)
plt.title("Mean Visibility vs Relative Humidities")
plt.xlabel("Relative Humidity (%)")
plt.ylabel("Mean Visibility (in miles to tenths)")

plt.show()
