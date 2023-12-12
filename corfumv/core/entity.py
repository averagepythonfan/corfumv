from abc import ABC, abstractmethod


class Entity(ABC):
    """Abstract entity class for experiments and models.
    
    Require a `rename` realization method, and `_prefix` property"""
    _prefix: str
    _create: str = "/create"
    _list: str = "/list"
    _find_by: str = "/find_by"
    _set: str = "/set"
    _delete: str = "/delete"

    @abstractmethod
    def rename(self, new_name: str):
        raise NotImplementedError()
    

    @abstractmethod
    def add_tag(self, tag: str):
        raise NotImplementedError()
    

    @abstractmethod
    def remove_tag(self, tag: str):
        raise NotImplementedError()