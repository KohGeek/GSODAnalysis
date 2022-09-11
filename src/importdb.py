import os
from argparse import ArgumentParser
from collections import OrderedDict

from dotenv import load_dotenv
import pandas as pd
import pymongo


def load_fips(country):
    # Load FIPS country codes
    fips = pd.read_csv(country, sep=r"\s{2,}", names=[
                       "CTRY", "CTRY_NAME"], engine='python')

    return fips


def load_station(station):
    # Load station data
    station = pd.read_csv(station, usecols=["USAF", "WBAN", "CTRY"],
                          dtype={"USAF": str, "WBAN": str})

    station = station.drop(station[station["CTRY"].isnull()].index)
    station = pd.concat((station, station.loc[:, ['USAF', 'WBAN']].apply(
        ''.join, axis=1).rename("STATION")), axis=1)
    station = station.set_index("STATION")

    return station


def load_data(folder, stationdata, database):
    # Load data from folder
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".csv"):
                weatherdata = pd.read_csv(os.path.join(root, file), usecols=[
                    "STATION", "DATE", "LATITUDE",
                    "LONGITUDE", "ELEVATION", "NAME",
                    "TEMP", "DEWP", "SLP", "STP",
                    "VISIB", "WDSP", "MXSPD", "GUST",
                    "MAX", "MIN", "PRCP", "SNDP", "FRSHTT"],
                    na_values=['9999.9', '999.9', '99.99'],
                    parse_dates=['DATE'], index_col=['DATE'],
                    infer_datetime_format=True, dtype={"STATION": str, "FRSHTT": str})

                if weatherdata["LATITUDE"][0] != 0.0:
                    print(f"{root}\\{file} processing")
                    station_id = weatherdata["STATION"][0]

                    try:
                        station = stationdata.loc[station_id]
                    except KeyError:
                        print(f"Station {station_id} not found")
                        continue

                    process_data(weatherdata, station, database)

                else:
                    print(f"{root}\\{file} skipped")


def process_data(data, station, database):
    station_id = data["STATION"][0]
    station_dict = station.to_dict()
    country = OrderedDict([("fips", station_dict["CTRY"]),
                           ("name", station_dict["CTRY_NAME"])])
    station_dict = OrderedDict([("_id", station_id), ("name", data["NAME"][0]),
                                ("usaf", station_dict["USAF"]),
                                ("wban", station_dict["WBAN"]),
                                ("country", country), ("location", {
                                    "type": "Point",
                                    "coordinates": [data["LONGITUDE"][0], data["LATITUDE"][0]]}),
                                ("elevation", data["ELEVATION"][0])])

    database["stations"].update_one(
        {"_id": station_id}, {"$set": station_dict}, upsert=True)

    data = data.drop(columns=["STATION", "NAME", "LATITUDE", "LONGITUDE",
                              "ELEVATION"])

    insert_query = []
    data_dict = data.to_dict(orient="index", into=OrderedDict)

    for key, value in data_dict.items():
        temp = value["FRSHTT"]
        indicators = OrderedDict([("fog", temp[0]), ("rain", temp[1]), ("snow", temp[2]),
                                  ("hail", temp[3]), ("thunder", temp[4]), ("tornado", temp[5])])
        del value["FRSHTT"]

        timestamp = key
        summary = OrderedDict()
        summary["temperature"] = value["TEMP"]
        summary["dewPoint"] = value["DEWP"]
        summary["seaLevelPressure"] = value["SLP"]
        summary["stationPressure"] = value["STP"]
        summary["visibility"] = value["VISIB"]
        summary["windSpeed"] = value["WDSP"]
        summary["maxSustainedWindSpeed"] = value["MXSPD"]
        summary["gust"] = value["GUST"]
        summary["maxTemperature"] = value["MAX"]
        summary["minTemperature"] = value["MIN"]
        summary["precipitation"] = value["PRCP"]
        summary["snowDepth"] = value["SNDP"]
        summary["indicators"] = indicators

        datarow = OrderedDict(
            [("station", station_dict), ("timestamp", timestamp)])
        datarow.update(summary)

        insert_query.append(datarow)

    try:
        database["weatherData"].insert_many(insert_query)
    except pymongo.errors.DuplicateKeyError as exception:
        print(exception)
    except pymongo.errors.BulkWriteError as exception:
        print(exception)


def parse_arg():
    parser = ArgumentParser(description='Import GSOD data into MongoDB')
    parser.add_argument(
        'folder', help='Folder containing GSOD data')
    parser.add_argument('country', help='Country FIPS file')
    parser.add_argument('station', help='ISD History file')

    return parser.parse_args()


def main():
    args = parse_arg()

    countrydata = load_fips(args.country)
    stationdata = load_station(args.station)
    stationdata = stationdata.reset_index().merge(
        countrydata, on=['CTRY'], how='left')
    stationdata = stationdata.set_index("STATION")

    # Load environment variables
    load_dotenv()

    admin_user = os.getenv('ADMIN_USER')
    admin_pass = os.getenv('ADMIN_PASS')
    host = os.getenv('HOST')
    port = os.getenv('PORT')

    # Connect to MongoDB
    client = pymongo.MongoClient(
        f"mongodb://{admin_user}:{admin_pass}@{host}:{port}/?authSource=admin",
        document_class=OrderedDict)

    database = client["gsod"]
    load_data(args.folder, stationdata, database)


if __name__ == "__main__":
    main()
