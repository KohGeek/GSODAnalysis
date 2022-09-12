import matplotlib.pyplot as plt
import pandas as pd

from src.tools.getdb import get_db

db = get_db().gsod

docs = db.weatherData.find({"station.location": {"$within": {"$box": [[100, 1], [104, 7]]}},
                            "station.elevation": {"$gt": 1000}},
                           {"temperature": 1, "seaLevelPressure": 1, "_id": 0})

data = pd.DataFrame(list(docs))

print(data)

x = data.iloc[:, 1]
y = data.iloc[:, 0]

plt.scatter(x, y, s=10)
plt.xlabel("Sea Level Pressure(0.1 mb)")
plt.ylabel("Temperature (F)")

plt.show()
