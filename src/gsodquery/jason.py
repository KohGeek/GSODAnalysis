import math

import pandas as pd
import matplotlib.pyplot as plt


def lat_elev_temp(database):
    """Query the database for latitude, elevation, and temperature data and plot it."""

    cols = database.weatherData

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

    for _, row in enumerate(coordinates):
        latitude = row
        latitudes.append(latitude[1])

    mean_temp = df1.iloc[:, -1]
    elevations = df1.iloc[:, 1]

    # Plot Graph

    _, axis = plt.subplots(figsize=(10, 6))
    plt.xlabel("Latitude (decimated degree)")
    plt.ylabel("Mean Temperature (Fahrenheit)")
    axis.scatter(x=latitudes, y=mean_temp)
    plt.title("Mean Temperature vs Latitude")

    plt.show()

    _, axis = plt.subplots(figsize=(10, 6))
    plt.xlabel("Latitude (decimated degree)")
    plt.ylabel("Mean Temperature (Fahrenheit)")
    axis.scatter(x=elevations, y=mean_temp)
    plt.title("Mean Temperature vs Elevation")

    plt.show()


def slp_wind(database):
    '''Query the database for sea level pressure and wind speed data and plot it.'''

    cols = database.weatherData

    docs = cols.aggregate([
        {"$limit": 1000000},
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

    mean_slp = df1.iloc[:, 0]
    # display(snowDepth)

    mean_wind = df1.iloc[:, 1]

    # Plot Graph

    _, axis = plt.subplots(figsize=(10, 6))
    axis.scatter(x=mean_slp, y=mean_wind)
    plt.title("Mean Wind Speed vs Mean Sea Level Pressure")
    plt.xlabel("Mean Sea Level Pressure (in millibars to tenths)")
    plt.ylabel("Mean Wind Speed (in knots to tenths)")

    plt.show()


def temp_snowdepth(database):
    '''Query the database for temperature and snow depth data and plot it.'''

    cols = database.weatherData

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

    mean_snow_depth = df1.iloc[:, 0]
    # display(snowDepth)

    mean_temp = df1.iloc[:, -1]

    # Plot Graph

    _, axis = plt.subplots(figsize=(10, 6))
    axis.scatter(x=mean_temp, y=mean_snow_depth)
    plt.title("Mean Snow Depth vs Mean Temperature")
    plt.xlabel("Mean Temperature (Fahrenheit)")
    plt.ylabel("Mean Snow Depth (inches)")

    plt.show()


def rh_visibility(database):
    '''Query the database for relative humidity and visibility data and plot it.'''

    cols = database.weatherData

    docs = cols.aggregate([
        {"$limit": 1000000},
        {"$match": {"$and": [
            {"visibility": {"$exists": True}},
            {"dewPoint": {"$exists": True}}
        ]}},
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

    mean_dews = df1.iloc[:, 0]
    mean_temp = df1.iloc[:, 1]
    mean_visibilities = df1.iloc[:, 2]

    # Calculating relative humidity
    relative_humidities = []

    for i in range(len(df1)):
        relative_humidity = 100*(math.exp((17.625*mean_dews[i])/(243.04+mean_dews[i]))
                                 / math.exp((17.625*mean_temp[i])/(243.04+mean_temp[i])))
        relative_humidities.append(relative_humidity)

    # Plot Graph

    _, axis = plt.subplots(figsize=(10, 6))
    axis.scatter(x=relative_humidities, y=mean_visibilities)
    plt.title("Mean Visibility vs Relative Humidities")
    plt.xlabel("Relative Humidity (%)")
    plt.ylabel("Mean Visibility (in miles to tenths)")

    plt.show()
