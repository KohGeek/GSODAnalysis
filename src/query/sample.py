from bson.son import SON

from src.tools.getdb import get_db


def main():

    client = get_db(1)

    collection = client["gsod"]["stations"]

    # Query the database
    query = collection.find(
        {"location": SON(
            [("$nearSphere", [3, 6]), ("$maxDistance", 30)])}
    )

    print(list(query))


if __name__ == "__main__":
    main()
