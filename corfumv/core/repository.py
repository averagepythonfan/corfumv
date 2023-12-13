from abc import ABC, abstractmethod
from typing import Iterable, TypeVar, Generic
from pydantic import BaseModel as PydanticBaseModel


PydanticModel = TypeVar("PydanticModel", bound=PydanticBaseModel)
AnyClient = TypeVar('AnyClient') 


# SYNC
class SyncRepository(Generic[PydanticModel, AnyClient], ABC):
    """Synchronous repository that impements CRUD pattern.
    Require pydantic model as `model` and client parameters.
    Session might passed as DatabaseClient: `MongoClient` as example."""


    @abstractmethod
    def save(self, obj: PydanticModel = None, **obj_data) -> bool:
        raise NotImplementedError("`create` method not implemented")
    

    @abstractmethod
    def get(self) -> Iterable[PydanticModel]:
        raise NotImplementedError("`read` method not implemented")
    

    @abstractmethod
    def update(self) -> bool:
        raise NotImplementedError("`update` method not implemented")
    

    @abstractmethod
    def delete(self) -> bool:
        raise NotImplementedError("`delete` method not implemented")


# ASYNC
class AsyncRepository(Generic[PydanticModel, AnyClient], ABC):
    """Asynchronous repository that impements CRUD pattern.
    Require pydantic model as `model` and session parameters.
    Session might passed as DatabaseClient: `MotorClient` as example."""


    @abstractmethod
    async def save(self):
        raise NotImplementedError("`create` method not implemented")
    

    @abstractmethod
    async def get(self):
        raise NotImplementedError("`read` method not implemented")
    

    @abstractmethod
    async def update(self):
        raise NotImplementedError("`update` method not implemented")
    

    @abstractmethod
    async def delete(self):
        raise NotImplementedError("`delete` method not implemented")
