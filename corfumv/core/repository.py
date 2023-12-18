from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

from pydantic import BaseModel as PydanticBaseModel

PydanticModel = TypeVar("PydanticModel", bound=PydanticBaseModel)
AnyClient = TypeVar("AnyClient")


class SyncRepository(Generic[PydanticModel, AnyClient], ABC):
    """Synchronous repository that impements CRUD pattern.

    Require pydantic model as `model` and client parameters.
    Session might passed as DatabaseClient: `MongoClient` as example.
    """

    @abstractmethod
    def save(self, obj: PydanticModel = None, **obj_data: dict) -> dict:
        """Save object to database.

        You may pass `pydantic` model or just object data."""
        raise NotImplementedError("`create` method not implemented")


    @abstractmethod
    def get(self, filter: dict, projection: dict) -> List[PydanticModel]:
        """Get instance by parameters.

        Return a list with models."""
        raise NotImplementedError("`read` method not implemented")


    @abstractmethod
    def update(self, filter: dict, update: dict) -> dict:
        raise NotImplementedError("`update` method not implemented")


    @abstractmethod
    def delete(self, filter) -> dict:
        raise NotImplementedError("`delete` method not implemented")


class AsyncRepository(Generic[PydanticModel, AnyClient], ABC):
    """Asynchronous repository that impements CRUD pattern.

    Require pydantic model as `model` and session parameters.
    Session might passed as DatabaseClient: `MotorClient` as example.
    """
    @abstractmethod
    async def save(self, obj: PydanticModel = None, **obj_data: dict):
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
