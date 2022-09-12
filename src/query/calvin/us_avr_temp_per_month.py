import matplotlib.pyplot as plt
import pandas as pd

from gsodtools.getdb import get_db

db = get_db().gsod

docs = db.weatherData.aggregate([
    {"$match": {"station.country.fips": "US"}},
    {"$group": {
        "_id": {"$month": "$timestamp"},
        "temperature": {"$avg": "$temperature"}
    }},
    {"$project": {
        "_id": 0,
        "month": "$_id",
        "temperature": "$temperature",
    }}])

data = pd.DataFrame(list(docs))

data.sort_values(by=['month'], inplace=True)

print(data)

x = data.iloc[:, 0]
y = data.iloc[:, 1]
labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

plt.bar(x, y, width=0.5, color='maroon')
plt.xticks(x, labels, rotation='vertical')
plt.xlabel("Month")
plt.ylabel("Temperature (F)")

plt.show()
