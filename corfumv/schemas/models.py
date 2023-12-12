from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Union, Dict, AnyStr, Any
from .misc import ObjectId, object_id_as_str


class MetaCollection(BaseModel):
    class Collection:
        name = None


# EXP
class Experiments(MetaCollection):

    id: ObjectId = Field(default_factory=object_id_as_str, alias="_id")
    name: Optional[str] = None
    tags: Optional[List[str]] = None
    date: datetime = datetime.now()
    models: Optional[List[ObjectId]] = []

    class Collection:
        name = "experiment"


# MODEL
class ModelParams(BaseModel):
    params: Optional[str] = None
    value: Optional[Union[int, float, str]] = None

class ModelMetrics(BaseModel):
    metric: Optional[str] = None
    value: Optional[Union[int, float]] = None

JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]


class Models(MetaCollection):

    id: ObjectId = Field(default_factory=object_id_as_str, alias="_id")
    params: Optional[List[ModelParams]] = None
    name: Optional[str] = None
    tags: Optional[List[str]] = None
    metrics: Optional[List[ModelMetrics]] = None
    description: Optional[str] = None
    date: datetime = datetime.now()
    config: Optional[JSONStructure] = None
    weights: Optional[JSONStructure] = None

    class Collection:
        name = "model"
