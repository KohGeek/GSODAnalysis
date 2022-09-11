import os
from argparse import ArgumentParser

from dotenv import load_dotenv
import pandas as pd
import pymongo


def parse_arg():
    parser = ArgumentParser(description='Import GSOD data into MongoDB')
    parser.add_argument(
        'folder', help='Folder containing GSOD data')
    parser.add_argument('country', help='Country FIPS file')
    parser.add_argument('station', help='ISD History file')

    return parser.parse_args()


def main():
    args = parse_arg()

    # Load environment variables
    load_dotenv()

    app_user = os.getenv('APP_USER')
    app_pass = os.getenv('APP_PASS')
    host = os.getenv('HOST')
    port = os.getenv('PORT')

    # Connect to MongoDB
    client = pymongo.MongoClient(
        f"mongodb://{app_user}:{app_pass}@{host}:{port}/?authSource=admin")

    collection = client["gsod"]["weatherData"]

    # Query the database
    query = collection.find(


if __name__ == "__main__":
    main()
