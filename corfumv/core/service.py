from abc import ABC, abstractmethod


class SyncCRUDService(ABC):

    @abstractmethod
    def create(self, obj):
        raise NotImplementedError


    @abstractmethod
    def read(self, instance, find_by, value, is_list: bool = False):
        raise NotImplementedError


    @abstractmethod
    def update(self,
               instance,
               instance_id,
               update,
               value):
        raise NotImplementedError


    @abstractmethod
    def delete(self, instance, instance_id):
        raise NotImplementedError
