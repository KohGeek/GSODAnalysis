import os
from argparse import ArgumentParser
from time import sleep

from dotenv import load_dotenv
import pandas as pd
import pymongo


def load_fips(country):
    # Load FIPS country codes
    fips = pd.read_csv(country, sep=r"\s{2,}", engine='python')

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


def load_data(folder, stationdata, collection):
    station_data_count = {}
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
                    infer_datetime_format=True)

                if weatherdata["LATITUDE"][0] != 0.0:
                    print(f"{root}\\{file} processing")
                    station_id = process_data(
                        weatherdata, stationdata, collection)

                else:
                    print(f"{root}\\{file} skipped")


def process_data(data, stationdata, collection):
    # Get station data

    return station_id


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

    print(countrydata)
    print(stationdata)

    # Load environment variables
    load_dotenv()

    admin_user = os.getenv('ADMIN_USER')
    admin_pass = os.getenv('ADMIN_PASS')
    host = os.getenv('HOST')
    port = os.getenv('PORT')

    # Connect to MongoDB
    client = pymongo.MongoClient(
        f"mongodb://{admin_user}:{admin_pass}@{host}:{port}/?authSource=admin")

    collection = client["gsod"]["weatherData"]
    load_data(args.folder, stationdata, collection)


if __name__ == "__main__":
    main()
