from bson import ObjectId
from requests import Session
from typing import Any, List, Optional, Type, Union, Dict
from corfumv.schemas import ExperimentsEntitry, ModelsEntity, FindBy, ModelParams
from corfumv.core import SyncClient


__all__ = [
    "RequestsClient"
]


ResponseJSONed = Union[Dict[str, Any], ConnectionError]


class BaseRequestsClient(SyncClient):

    session: Type[Session]

    experiment_entity: Type[ExperimentsEntitry] = ExperimentsEntitry
    model_entity: Type[ModelsEntity] = ModelsEntity

    _exp_endpoint: str = "/experiments"
    _model_endpoint: str = "/models"

    _create: str = "/create"
    _list: str = "/list"
    _find: str = "/find_by"
    _set: str = "/set"
    _delete: str = "/delete"


    def __init__(self,
                 uri: Optional[str]) -> None:
        self._uri = uri


    def __make_request(self, options: dict) -> ResponseJSONed:
        with self.session() as session:
            resp = session.request(**options)
            if resp.status_code == 200:
                return resp.json()
            else:
                raise ConnectionError(resp.text)


    @property
    def uri(self) -> str:
        """Return `uri` property."""
        return self._uri
        

    def create_experiment(self, name: str, tags: List[str]) -> ExperimentsEntitry:
        hex_id = ObjectId().binary.hex()
        options = {
            "method": "POST",
            "url": self._uri + self._exp_endpoint + self._create,
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
        hex_id = ObjectId().binary.hex()
        options = {
            "method": "POST",
            "url": self._uri + self._model_endpoint + self._create,
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
        resp =  self._list_of(
            prefix=self._exp_endpoint,
            page=page,
            number_of=number_of
        )
        return [self.experiment_entity(**el, uri=self._uri) for el in resp]


    def list_of_models(self,
                       page: int = 0,
                       number_of: int = 10) -> List[ModelsEntity]:
        resp = self._list_of(
            prefix=self._model_endpoint,
            page=page,
            number_of=number_of
        )
        return [self.model_entity(**el, uri=self._uri) for el in resp]


    def _find_by(self,
                 endpoint: str,
                 instance: Union[ExperimentsEntitry, ModelsEntity],
                 find_by: Union[str, FindBy],
                 value: Union[str, float],
                 is_list: bool = False) -> List[Union[ExperimentsEntitry, ModelsEntity]]:
        """Private method to find instance BY."""
        find = find_by if isinstance(find_by, FindBy) else FindBy(find_by)
        options = {
            "method": "GET",
            "url": self.uri + endpoint + self._find,
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


    def find_experiment_by(self, find_by, value, is_list: bool = False) -> Union[ExperimentsEntitry, List[ExperimentsEntitry]]:
        return self._find_by(
            endpoint=self._exp_endpoint,
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
            endpoint=self._model_endpoint,
            instance=self.model_entity,
            find_by=find_by,
            value=value,
            is_list=is_list
        )


class RequestsClient(BaseRequestsClient):

    session = Session