import matplotlib.pyplot as plt
import pandas as pd

from src.tools.getdb import get_db

db = get_db().gsod

docs = db.weatherData.aggregate([
    {"$match": {"station.country.fips": "US"}},
    {"$group": {
        "_id": {"$year": "$timestamp"},
        "precipitation": {"$avg": "$precipitation"}
    }},
    {"$project": {
        "_id": 0,
        "year": "$_id",
                "precipitation": "$precipitation",
    }}])

data = pd.DataFrame(list(docs))

data.sort_values(by=['year'], inplace=True)

print(data)

x = data.iloc[:, 0]
y = data.iloc[:, 1]
labels = ['2016', '2017', '2018', '2019', '2020', '2021']

plt.plot(x, y)
plt.xticks(x, labels, rotation='vertical')
plt.xlabel("Year")
plt.ylabel("Precipitation (0.01 inches)")

plt.show()
