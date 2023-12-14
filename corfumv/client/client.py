from typing import Any, List, Type, TypeVar, Union

from bson import ObjectId
from requests import Session

from corfumv.schemas import (
    CreationResponse,
    ExperimentsEntitry,
    FindBy,
    ModelParams,
    ModelsEntity,
)
from corfumv.utils import get_corfumv_server_uri

T = TypeVar("T")
FindByResponse = Union[T, List[T]]


class CorfuClient:
    """Main CorfuMV client sync interface.

    Make request with `requests` lib.
    """

    session: Type[Session]

    def __init__(self,
                 uri: str = None,
                 session: Type[Session] = Session) -> None:
        self._session: Session = session
        self._uri = uri if uri else get_corfumv_server_uri()
        self._exp_endpoint = "/experiments"
        self._model_endpoint = "/models"

    @property
    def uri(self):
        return self._uri

    def create_experiment(self,
                          name: str,
                          tags: List[str],
                          object_id: ObjectId = ObjectId()) -> ExperimentsEntitry:
        """Pass experiment name and tags.

        Create experiments with CorfuMV server.
        """
        hex_id = object_id.binary.hex()

        url = self._uri + self._exp_endpoint + "/create"
        json_data = {
            "_id": hex_id,
            "name": name,
            "tags": tags,
        }
        with self._session() as session:
            session: Session
            resp = session.request("POST", url, json=json_data)
            if resp.status_code == 200:
                resp = CreationResponse(**resp.json())
                assert resp.object_id == hex_id
                return ExperimentsEntitry(
                    _id=hex_id,
                    name=name,
                    tags=tags,
                    uri=self._uri
                )
            else:
                raise TypeError(resp.text)


    def create_model(self,
                     name: str,
                     tags: List[str],
                     params: List[ModelParams] = None,
                     description: str = "",
                     object_id: ObjectId = ObjectId()) -> ModelsEntity:
        """Pass model name and tags.

        Also you mau pass params options.
        Create model with CorfuMV server.
        """
        hex_id = object_id.binary.hex()

        url = self._uri + self._model_endpoint + "/create"
        json_data = {
            "_id": hex_id,
            "name": name,
            "tags": tags,
            "params": [el.model_dump() for el in params] if params else [],
            "description": description
        }
        with self._session() as session:
            session: Session
            resp = session.request("POST", url, json=json_data)
            if resp.status_code == 200:
                resp = CreationResponse(**resp.json())
                assert resp.object_id == hex_id
                return ModelsEntity(
                    _id=hex_id,
                    name=name,
                    tags=tags,
                    params=params,
                    description=description,
                    uri=self._uri
                )
            else:
                raise TypeError(resp.text)


    def list_of_experiments(self,
                            page: int = 0,
                            number_of: int = 10) -> List[ExperimentsEntitry]:
        url = self._uri + self._exp_endpoint + "/list"
        params = {
            "num": number_of,
            "page": page,
        }
        with self._session() as session:
            resp = session.request("GET", url, params=params)
            if resp.status_code == 200:
                return [ExperimentsEntitry(**el) for el in resp.json()]
            else:
                return resp.json()


    def list_of_models(self, page: int = 0, number_of: int = 10):
        url = self._uri + self._model_endpoint + "/list"
        params = {
            "num": number_of,
            "page": page,
        }
        with self._session() as session:
            resp = session.request("GET", url, params=params)
            if resp.status_code == 200:
                return [ModelsEntity(**el) for el in resp.json()]
            else:
                return resp.json()


    def _find_by(self,
                 endpoint: str,
                 instance: Union[ExperimentsEntitry, ModelsEntity],
                 find_by: Union[str, FindBy],
                 value: Any,
                 is_list: bool = False) -> List[T]:
        """Private method to find instance BY."""
        find = find_by if isinstance(find_by, FindBy) else FindBy(find_by)
        options = {
            "method": "GET",
            "url": self.uri + endpoint + "/find_by" ,
            "params": {
                "find_by": find.value,
                "value": value,
                "is_list": is_list,
            }
        }
        with self._session() as session:
            session: Session
            resp = session.request(**options)
            if resp.status_code == 200:
                if is_list is False:
                    return instance(**resp.json()[0])
                else:
                    return [instance(**el) for el in resp.json()]
            else:
                raise ConnectionError(resp.text)


    def find_experiment_by(self,
                           find_by: Union[str, FindBy],
                           value: Any,
                           is_list: bool = False) -> FindByResponse[ExperimentsEntitry]:
        return self._find_by(
            endpoint=self._exp_endpoint,
            instance=ExperimentsEntitry,
            find_by=find_by,
            value=value,
            is_list=is_list
        )


    def find_model_by(self,
                      find_by: Union[str, FindBy],
                      value: Any,
                      is_list: bool = False) -> FindByResponse[ModelsEntity]:
        return self._find_by(
            endpoint=self._model_endpoint,
            instance=ModelsEntity,
            find_by=find_by,
            value=value,
            is_list=is_list
        )


    def __enter__(self):
        self.session = self._session()
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        self._session.close()
