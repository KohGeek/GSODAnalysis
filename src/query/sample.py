import os
from argparse import ArgumentParser
from bson.son import SON

from dotenv import load_dotenv
import pandas as pd
import pymongo


def parse_arg():
    parser = ArgumentParser()
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

    collection = client["gsod"]["stations"]

    # Query the database
    query = collection.find(
        {"location": SON(
            [("$nearSphere", [3, 6]), ("$maxDistance", 30)])}
    )

    print(list(query))


if __name__ == "__main__":
    main()
