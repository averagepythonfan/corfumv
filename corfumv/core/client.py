from abc import ABC, abstractmethod
from typing import Type, TypeVar


SyncSession = TypeVar("SyncSession")
AsyncSession = TypeVar("AsyncSession")

ExpEntity = TypeVar("ExpEntity")
MdEntity = TypeVar("MdEntity")


class SyncClient(ABC):

    session: Type[SyncSession]

    experiment_entity: Type[ExpEntity]
    model_entity: Type[MdEntity]


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

    session: Type[AsyncSession]

    experiment_entity: Type[ExpEntity]
    model_entity: Type[MdEntity]


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
