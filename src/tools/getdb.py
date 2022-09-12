import os

from dotenv import load_dotenv
import pymongo


def get_db(type=0):
    '''
    Get database connection
    Type indicates admin or user credential. 0 = user, 1 = admin.
    '''

    # Load environment variables
    load_dotenv()

    if type == 0:
        username = os.getenv('APP_USER')
        password = os.getenv('APP_PASS')
    elif type == 1:
        username = os.getenv('ADMIN_USER')
        password = os.getenv('ADMIN_PASS')
    else:
        raise Exception("Invalid type")

    host = os.getenv('HOST')
    port = os.getenv('PORT')

    # Connect to MongoDB
    return pymongo.MongoClient(
        f"mongodb://{username}:{password}@{host}:{port}/?authSource=admin")
