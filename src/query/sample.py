import os
from bson.son import SON

from dotenv import load_dotenv
import pymongo


def main():
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
