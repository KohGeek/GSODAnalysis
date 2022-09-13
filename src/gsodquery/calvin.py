import matplotlib.pyplot as plt
import pandas as pd


def temp_pressure(database):
    """Query the database for temperature and pressure data and plot it."""

    docs = database.weatherData.find({"station.location": {"$within": {"$box": [[100, 1], [104, 7]]}},
                                      "station.elevation": {"$gt": 1000}},
                                     {"temperature": 1, "seaLevelPressure": 1, "_id": 0})

    data = pd.DataFrame(list(docs))

    x_axis = data.iloc[:, 1]
    y_axis = data.iloc[:, 0]

    plt.scatter(x_axis, y_axis, s=10)
    plt.xlabel("Sea Level Pressure(0.1 mb)")
    plt.ylabel("Temperature (F)")

    plt.show()


def avr_precipitation(database):
    """Query the database for US precipitation data and plot it."""

    docs = database.weatherData.aggregate([
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

    x_axis = data.iloc[:, 0]
    y_axis = data.iloc[:, 1]
    labels = ['2016', '2017', '2018', '2019', '2020', '2021']

    plt.plot(x_axis, y_axis)
    plt.xticks(x_axis, labels, rotation='vertical')
    plt.xlabel("Year")
    plt.ylabel("Precipitation (0.01 inches)")

    plt.show()


def avr_temp(database):
    """Query the database for US temperature data and plot it."""

    docs = database.weatherData.aggregate([
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

    x_axis = data.iloc[:, 0]
    y_axis = data.iloc[:, 1]
    labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    plt.bar(x_axis, y_axis, width=0.5, color='maroon')
    plt.xticks(x_axis, labels, rotation='vertical')
    plt.xlabel("Month")
    plt.ylabel("Temperature (F)")

    plt.show()
