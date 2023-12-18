from abc import ABC, abstractmethod
from typing import Optional, Type, TypeVar


SyncSession = TypeVar("SyncSession")
AsyncSession = TypeVar("AsyncSession")

ExpEntity = TypeVar("ExpEntity")
MdEntity = TypeVar("MdEntity")


class SyncClient(ABC):

    session: Type[SyncSession]

    experiment_entity: Type[ExpEntity]
    model_entity: Type[MdEntity]

    def __init__(self,
                 uri: Optional[str]) -> None:
        self._uri = uri


    @property
    def uri(self) -> str:
        """Return `uri` property."""
        return self._uri


    @abstractmethod
    def create_experiment(self):
        raise NotImplementedError()
    
    @abstractmethod
    def create_model(self):
        raise NotImplementedError()

    @abstractmethod
    def list_of_experiments(self):
        raise NotImplementedError()
    
    @abstractmethod
    def list_of_models(self):
        raise NotImplementedError()
    
    @abstractmethod
    def find_experiment_by(self):
        raise NotImplementedError()
    
    @abstractmethod
    def find_model_by(self):
        raise NotImplementedError()


class AsyncClient(ABC):

    session: Type[SyncSession]

    experiment_entity: Type[ExpEntity]
    model_entity: Type[MdEntity]

    def __init__(self,
                 uri: Optional[str]) -> None:
        self._uri = uri


    @property
    def uri(self) -> str:
        """Return `uri` property."""
        return self._uri

    @abstractmethod
    async def create_experiment(self):
        raise NotImplementedError()
    
    @abstractmethod
    async def create_model(self):
        raise NotImplementedError()

    @abstractmethod
    async def list_of_experiments(self):
        raise NotImplementedError()
    
    @abstractmethod
    async def list_of_models(self):
        raise NotImplementedError()
    
    @abstractmethod
    async def find_experiment_by(self):
        raise NotImplementedError()
    
    @abstractmethod
    async def find_model_by(self):
        raise NotImplementedError()
