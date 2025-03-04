# from typing import Annotated, Any, Dict, Optional, Union

# from bson import ObjectId
# from pydantic import BaseModel, ConfigDict, Field
# from pydantic.functional_serializers import PlainSerializer

# ObjectIdSerializer = PlainSerializer(
#     lambda x: str(x),
#     return_type=str,
#     when_used="json",
# )

# ObjectIdField = Annotated[Union[ObjectId, str], ObjectIdSerializer]


# class MongoDBBaseModel(BaseModel):
#     id: Optional[ObjectIdField] = Field(default=None)
#     model_config = ConfigDict(
#         populate_by_name=True,
#         arbitrary_types_allowed=True,
#         json_encoders={ObjectId: str},
#     )

#     def __init__(self, **data):
#         if "_id" in data:
#             data["id"] = data.pop("_id")
#         super().__init__(**data)

#     def to_mongodb_dictionary(self) -> Dict[str, Any]:
#         data = self.model_dump(exclude_none=True, exclude={"id"})

#         if self.id is not None:
#             _id = ObjectId(self.id) if isinstance(self.id, str) else self.id
#             data["_id"] = _id

#         return data

from typing import Annotated, Any, Dict, Optional, Union

from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel, ConfigDict, Field
from pydantic.functional_serializers import PlainSerializer

ObjectIdSerializer = PlainSerializer(
    lambda x: str(x),
    return_type=str,
    when_used="json",
)

ObjectIdField = Annotated[Union[ObjectId, str], ObjectIdSerializer]


class MongoDBBaseModel(BaseModel):
    id: Optional[ObjectIdField] = Field(default=None)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

    def __init__(self, **data):
        if "_id" in data:
            data["id"] = data.pop("_id")
        super().__init__(**data)

    def to_mongodb_dictionary(self) -> Dict[str, Any]:
        data = self.model_dump(exclude_none=True, exclude={"id"})

        if self.id is not None:
            try:
                if isinstance(self.id, str):
                    _id = ObjectId(self.id)
                    data["_id"] = _id
                else:
                    data["_id"] = self.id
            except InvalidId:
                pass

        return data
