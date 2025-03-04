from typing import Any, Dict, Optional, Type, Union

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel

from foundation.v1 import CustomLogger

from .mongodb_base_model import MongoDBBaseModel
from .mongodb_client import MongoDBClient

logger = CustomLogger(log_level="INFO")


class classproperty:
    def __init__(self, method):
        self.method = method

    def __get__(self, instance, cls):
        return self.method(cls)


class DataModelHandler:
    DB_NAME: str
    COLLECTION_NAME: str

    _mongodb_client: Optional[MongoDBClient] = None
    _collection: Optional[AsyncIOMotorCollection] = None

    @classmethod
    def _get_mongodb_client(cls) -> MongoDBClient:
        if cls._mongodb_client is None:
            cls._mongodb_client = MongoDBClient()
        return cls._mongodb_client

    @classproperty
    def collection(cls) -> AsyncIOMotorCollection:
        if cls._collection is None:
            cls._collection = cls._get_mongodb_client().get_collection(cls.DB_NAME, cls.COLLECTION_NAME)
        return cls._collection

    @classmethod
    async def insert(cls, data: Union[Dict, MongoDBBaseModel]) -> ObjectId:
        try:
            result = await cls.collection.insert_one(
                data if isinstance(data, dict) else data.to_mongodb_dictionary()
            )
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error inserting document: {e}")
            raise

    @classmethod
    async def update_one(
        cls,
        filter_criteria: Dict[str, Any],
        update_data: Dict[str, Any],
        upsert: bool = False,
    ) -> Dict[str, Any]:
        try:
            if "_id" in filter_criteria and isinstance(filter_criteria["_id"], str):
                filter_criteria["_id"] = ObjectId(filter_criteria["_id"])

            if not any(key.startswith("$") for key in update_data.keys()):
                raise ValueError(
                    "update_data must contain at least one MongoDB update operator ($set, $inc, etc.)"
                )

            result = await cls.collection.update_one(filter_criteria, update_data, upsert=upsert)

            update_result = {
                "modified_count": result.modified_count,
                "matched_count": result.matched_count,
                "upserted_id": result.upserted_id,
            }

            return update_result

        except Exception as e:
            logger.error(f"Error updating document: {e}")
            raise

    @classmethod
    async def load(cls, document_id: str | None = None, model_type: Type[BaseModel] | None = None) -> Any | None:
        if document_id is None:
            documents = await cls.collection.find().to_list(length=None)
            if model_type is not None:
                return [model_type.model_validate(doc) for doc in documents]
            return documents

        document = await cls.collection.find_one({"_id": ObjectId(document_id)})
        if document is None:
            return None

        if model_type is not None:
            return model_type.model_validate(document)
        return document
