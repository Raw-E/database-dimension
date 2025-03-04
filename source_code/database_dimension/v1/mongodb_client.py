import os

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from foundation.v1 import CustomLogger, SingletonMetaclass

logger = CustomLogger(log_level="INFO")


class MongoDBClient(metaclass=SingletonMetaclass):
    def __init__(self) -> None:
        uri = f"mongodb+srv://{os.getenv('MONGODB_ATLAS_USERNAME', '')}:{os.getenv('MONGODB_ATLAS_PASSWORD', '')}@{os.getenv('MONGODB_ATLAS_CLUSTER_ADDRESS', '')}/?retryWrites=true&w=majority&appName={os.getenv('MONGODB_ATLAS_CLUSTER_NAME', '')}"
        self._client: AsyncIOMotorClient = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)

    def get_collection(self, database_name: str, collection_name: str) -> AsyncIOMotorCollection:
        return self._client[database_name][collection_name]

    def close(self) -> None:
        self._client.close()
