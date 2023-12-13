from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Union, Dict, AnyStr, Any
from .misc import ObjectId, object_id_as_str


class MetaCollection(BaseModel):
    class Collection:
        name = None


class Experiments(MetaCollection):
    """Experiments base model.
    
    Uses as instance for any repository.
    For example:
    >>> class SyncExperimentRepository(PymongoRepository):
    ...     model = Experiments
    
    Requires set `class Collcection` and property `name`.
    Might be used in client section."""

    id: ObjectId = Field(default_factory=object_id_as_str, alias="_id")
    name: Optional[str] = None
    tags: Optional[List[str]] = None
    date: datetime = datetime.now()
    models: Optional[List[ObjectId]] = []

    class Collection:
        name = "experiment"


class ModelParams(BaseModel):
    parameter: Optional[str] = None
    value: Optional[Union[int, float, str]] = None

class ModelMetrics(BaseModel):
    metric: Optional[str] = None
    value: Optional[Union[int, float]] = None

JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]


class Models(MetaCollection):
    """Models base model.
    
    Uses as instance for any repository.
    For example:
    >>> class SyncExperimentRepository(PymongoRepository):
    ...     model = Models
    
    Requires set `class Collcection` and property `name`.
    Might be used in client section."""

    id: ObjectId = Field(default_factory=object_id_as_str, alias="_id")
    name: Optional[str] = None
    params: Optional[List[ModelParams]] = None
    tags: Optional[List[str]] = None
    metrics: Optional[List[ModelMetrics]] = None
    description: Optional[str] = None
    date: datetime = datetime.now()
    config: Optional[JSONStructure] = None
    weights: Optional[JSONStructure] = None

    class Collection:
        name = "model"
