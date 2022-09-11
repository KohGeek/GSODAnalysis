import pymongo
import matplotlib.pyplot as plt
import pandas as pd

db = pymongo.MongoClient("mongodb://gsod:1234@0.tcp.ap.ngrok.io:17088").gsod

docs = db.weatherData.find({"station.location": {"$within": {"$box": [[100, 1], [104, 7]]}}, "station.elevation": {"$gt": 1000}}, {"temperature":1,"seaLevelPressure":1,"_id":0})

data = pd.DataFrame(list(docs))

print(data)

x = data.iloc[:,0]
y = data.iloc[:,1]

plt.scatter(x, y, s=10)
plt.xlabel("Sea Level Pressure(0.1 mb)")
plt.ylabel("Temperature (F)")

plt.show()