from abc import ABC, abstractmethod
from typing import Type, TypeVar, Union, final

from .repository import SyncRepository

ExperimentRepository = TypeVar("ExperimentRepository")
ModelRepository = TypeVar("ModelRepository")
AnyRepository = Union[ExperimentRepository, ModelRepository]


class SyncUnitOfWork(ABC):
    """Synchronous unit of work interface.
    Uses as superclass for every sync interface.

    Examples
    --------
        >>> class PymongoUnitOfWork(SyncUnitOfWork):
        >>> ...

        >>> class RedisUnitOfWork(SyncUnitOfWork):
        >>> ...

    It require a definition of several methods:
    - `__init__`
    - `__enter__` and `__exit___` for context manager
    - `commit` and `rollback` for transactions
    """

    experiment: Type[SyncRepository]
    model: Type[SyncRepository]

    def __init__(self,
                 autocommit: bool = False) -> None:
        """Definitely requires a repository instance,
        optional you may pass `autocommit` bool parameter.
        """
        self.autocommit = autocommit


    def __enter__(self):
        self.begin()
        return self


    @final
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
            raise exc_val
        else:
            if self.autocommit:
                self.commit()
            self.close()


    @abstractmethod
    def begin(self):
        raise NotImplementedError


    @abstractmethod
    def commit(self):
        raise NotImplementedError


    @abstractmethod
    def rollback(self):
        raise NotImplementedError


    @abstractmethod
    def close(self):
        raise NotImplementedError


# ASYNC
class AsyncUnitOfWork(ABC):


    def __init__(self,
                 repository: AnyRepository,
                 autocommit: bool = False) -> None:
        """Definitely requires a repository instance,
        optional you may pass `autocommit` bool parameter.
        """
        self.repository = repository
        self.autocommit = autocommit


    @abstractmethod
    async def __aenter__(self):
        await self.begin()
        return self

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
            raise exc_val
        else:
            if self.autocommit:
                await self.commit()
            await self.close()

    @abstractmethod
    async def begin(self):
        raise NotImplementedError


    @abstractmethod
    async def commit(self):
        raise NotImplementedError


    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


    @abstractmethod
    async def close(self):
        raise NotImplementedError
