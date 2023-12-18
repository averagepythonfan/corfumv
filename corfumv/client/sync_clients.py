from typing import Any, Dict, List, Optional, Type, Union

from bson import ObjectId
from requests import Session

from corfumv.core import SyncClient
from corfumv.schemas import ExperimentsEntitry, FindBy, ModelParams, ModelsEntity

__all__ = [
    "RequestsClient"
]


ResponseJSONed = Union[Dict[str, Any], ConnectionError]


class BaseRequestsClient(SyncClient):
    """Base synchromous class for requests."""

    session: Type[Session]

    experiment_entity: Type[ExperimentsEntitry] = ExperimentsEntitry
    model_entity: Type[ModelsEntity] = ModelsEntity

    _create: str = "/create"
    _list: str = "/list"
    _find: str = "/find_by"
    _set: str = "/set"
    _delete: str = "/delete"


    def __init__(self, uri: Optional[str]) -> None:
        super(BaseRequestsClient, self).__init__(uri=uri)


    def __make_request(self, options: dict) -> ResponseJSONed:
        """Base private request method. Require a dict with
        `method`, `url` and `params`/`json` data."""

        with self.session() as session:
            resp = session.request(**options)
            if resp.status_code == 200:
                return resp.json()
            else:
                raise ConnectionError(resp.text)


    def create_experiment(self, name: str, tags: List[str]) -> ExperimentsEntitry:
        """Create experiment and return its instance."""

        hex_id = ObjectId().binary.hex()

        options = {
            "method": "POST",
            "url": self._uri + self.experiment_entity.Collection.endpoint + self._create,
            "json": {
                "_id": hex_id,
                "name": name,
                "tags": tags,
            }
        }
        if self.__make_request(options=options):
                return self.experiment_entity(
                    _id=hex_id,
                    name=name,
                    tags=tags,
                    uri=self._uri
                )


    def create_model(self,
                     name: str,
                     tags: List[str],
                     params: Optional[List[ModelParams]] = None,
                     description: str = "") -> ModelsEntity:
        """Create model and return its instance."""

        hex_id = ObjectId().binary.hex()

        options = {
            "method": "POST",
            "url": self._uri + self.model_entity.Collection.endpoint + self._create,
            "json": {
                "_id": hex_id,
                "name": name,
                "tags": tags,
                "params": [el.model_dump() for el in params] if params else [],
                "description": description
            }
        }
        if self.__make_request(options=options):
            return self.model_entity(
                _id=hex_id,
                name=name,
                tags=tags,
                description=description,
                uri=self._uri
            )


    def _list_of(self, prefix: str, page: int = 0, number_of: int = 10) -> list:
        """Private method that return list of set instances."""

        options = {
            "method": "GET",
            "url": self._uri + prefix + self._list,
            "params": {
                "num": number_of,
                "page": page,
            }
        }
        return self.__make_request(options=options)


    def list_of_experiments(self,
                            page: int = 0,
                            number_of: int = 10) -> List[ExperimentsEntitry]:
        """Return a list of all existing experiments."""

        resp =  self._list_of(
            prefix=self.experiment_entity.Collection.endpoint,
            page=page,
            number_of=number_of
        )
        return [self.experiment_entity(**el, uri=self._uri) for el in resp]


    def list_of_models(self,
                       page: int = 0,
                       number_of: int = 10) -> List[ModelsEntity]:
        """Return a list of all existing models."""

        resp = self._list_of(
            prefix=self.model_entity.Collection.endpoint,
            page=page,
            number_of=number_of
        )
        return [self.model_entity(**el, uri=self._uri) for el in resp]


    def _find_by(self,
                 instance: Union[ExperimentsEntitry, ModelsEntity],
                 find_by: Union[str, FindBy],
                 value: Union[str, float],
                 is_list: bool = False) -> List[Union[ExperimentsEntitry, ModelsEntity]]:
        """Private method to find instance BY."""

        find = find_by if isinstance(find_by, FindBy) else FindBy(find_by)

        options = {
            "method": "GET",
            "url": self.uri + instance.Collection.endpoint + self._find,
            "params": {
                "find_by": find.value,
                "value": value,
                "is_list": is_list,
            }
        }
        if resp := self.__make_request(options=options):
            resp: List[Union[ExperimentsEntitry, ModelsEntity]]
            if is_list is False:
                if len(resp) == 1:
                    return instance(**resp[0], uri=self._uri)
                else:
                    TypeError("Multiple data, but flag `is_list` is False")
            else:
                return [
                    instance(**el, uri=self._uri) for el in resp
                ]


    def find_experiment_by(self,
                           find_by,
                           value,
                           is_list: bool = False) -> Union[ExperimentsEntitry, List[ExperimentsEntitry]]:
        return self._find_by(
            instance=self.experiment_entity,
            find_by=find_by,
            value=value,
            is_list=is_list
        )


    def find_model_by(self,
                      find_by,
                      value,
                      is_list: bool = False) -> Union[ModelsEntity, List[ModelsEntity]]:
        return self._find_by(
            instance=self.model_entity,
            find_by=find_by,
            value=value,
            is_list=is_list
        )


class RequestsClient(BaseRequestsClient):
    """Final sync client class."""

    session = Session
