from pymongo import MongoClient

from app.core.settings import settings

client = MongoClient(settings.mongo_uri)

db = client[settings.mongo_db]
