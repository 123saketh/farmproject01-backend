from motor.motor_asyncio import AsyncIOMotorClient
from .constants import mongoDbUrl

class MongoDB:
    def __init__(self, db_name: str, collection_name: str):
        self.client = AsyncIOMotorClient(mongoDbUrl)
        self.database = self.client[db_name]
        self.collection = self.database[collection_name]

    def get_collection(self):
        return self.collection