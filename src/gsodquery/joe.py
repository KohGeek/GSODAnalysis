import pandas as pd

def max_gust(database):
    '''Query the database for the top 20 highest wind gusts and print them.'''

    docs = database.weatherData.aggregate([
        {"$sort": {"gust": -1}},
        {"$limit": 20},
        {"$project": {
            "_id": 0,
            "Top 20 Highest Gust": "$gust",
            "Country": "$station.country.name",
            "Station": "$station.name"
        }}
    ])

    dataframe = pd.DataFrame(list(docs))
    print(dataframe)


def max_temp(database):
    '''Query the database for the top 20 highest temperatures and print them.'''

    docs = database.weatherData.aggregate([
        {"$sort": {"temperature": -1}},
        {"$limit": 20},
        {"$project": {
            "_id": 0,
            "Top 20 Highest Temperature": "$temperature",
            "Country": "$station.country.name",
            "Station": "$station.name"
        }}
    ])

    dataframe = pd.DataFrame(list(docs))
    print(dataframe)
    

def min_temp(database):
    '''Query the database for the top 20 lowest temperatures and print them.'''

    docs = database.weatherData.aggregate([
        {"$sort": {"temperature": 1}},
        {"$limit": 20},
        {"$project": {
            "_id": 0,
            "Top 20 Lowest Temperature": "$temperature",
            "Country": "$station.country.name",
            "Station": "$station.name"
        }}
    ])

    dataframe = pd.DataFrame(list(docs))
    print(dataframe)
    

def max_precip(database):
    '''Query the database for the top 20 highest precipitation and print them.'''

    docs = database.weatherData.aggregate([
        {"$sort": {"precipitation": -1}},
        {"$limit": 20},
        {"$project": {
            "_id": 0,
            "Top 20 Highest Precipitation": "$precipitation",
            "Country": "$station.country.name",
            "Station": "$station.name"
        }}
    ])

    dataframe = pd.DataFrame(list(docs))
    print(dataframe)
    
    