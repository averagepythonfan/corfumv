from abc import ABC, abstractmethod
from requests import Session
from typing import Any, List, Type, Union
from corfumv.schemas import FindBy, DeletionResponse, UpdationResponse, UpdateExperiment


class Entity(ABC):
    """Abstract entity class for experiments and models.
    
    Require a `rename` realization method, and `_prefix` property.
    Class implements `rename`, `add_tag`, `remove_tag` and `delete` method."""

    uri: str
    _prefix: str
    _create: str = "/create"
    _list: str = "/list"
    _find_by: str = "/find_by"
    _set: str = "/set"
    _delete: str = "/delete"
    _session: Type[Session] = Session


    def _make_request(self, **options) -> dict | ConnectionError:
        with self._session() as session:
            resp = session.request(**options)
            if resp.status_code == 200:
                return resp.json()
            else:
                raise ConnectionError(resp.text)


    def _patch_request(self, update: str, value: str) -> dict:
        options = {
            "method": "PATCH",
            "url": self.uri + self._prefix + self._set ,
            "params": {
                'instance_id': self.id,
                'update': update,
                'value': value,
            }
        }
        return self._make_request(**options)


    def rename(self, new_name: str) -> UpdationResponse:
        return self._patch_request(
            update=UpdateExperiment.rename.value,
            value=new_name
        )


    def add_tag(self, tag: str) -> UpdationResponse:
        return self._patch_request(update="add_tag", value=tag)
    

    def remove_tag(self, tag: str) -> UpdationResponse:
        return self._patch_request(update="remove_tag", value=tag)
    

    def find_by(self,
                find_by: Union[str, FindBy],
                value: Any,
                is_list: bool = False) -> List[dict]:
        find = find_by if isinstance(find_by, FindBy) else FindBy(find_by)
        options = {
            "method": "GET",
            "url": self.uri + self._prefix + self._set ,
            "params": {
                'find_by': find.value,
                'value': value,
                'is_list': is_list,
            }
        }
        return self._make_request(**options)


    def delete(self) -> DeletionResponse:
        options = {
            "method": "DELETE",
            "url": self.uri + self._prefix + self._delete,
            "params": {
                'instance_id': self.id,
            }
        }
        return self._make_request(**options)