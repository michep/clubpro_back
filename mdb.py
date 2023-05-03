from pymongo.mongo_client import MongoClient
from pymongo.database import Database
from config import MONGODB_CONNECTION


MDB: Database = MongoClient(MONGODB_CONNECTION).get_database('clubpro')
