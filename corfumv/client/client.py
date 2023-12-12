from typing import Type, List
from requests import Session
from corfumv.utils import get_corfumv_server_uri
from corfumv.schemas import ExperimentsEntitry, ModelsEntity, Experiments


class CorfuClient:

    session: Type[Session]

    def __init__(self, uri: str = None, session: Type[Session] = Session):
        self._session: Session = session
        self._uri = uri if uri else get_corfumv_server_uri()
        self._exp_endpoint = "/experiments"
        self._model_endpoint = "/models"

    @property
    def uri(self):
        return self._uri

    def create_experiment(self, name: str, tags: List[str]) -> Experiments:
        url = self._uri + self._exp_endpoint + "/create"
        json_data = {
            'name': name,
            'tags': tags,
        }
        with self._session() as session:
            resp = session.request("POST", url, json=json_data)
            if resp.status_code == 200:
                return ExperimentsEntitry(name=name, tags=tags)
            else:
                raise TypeError(resp.text())


    def list_of_experiments(self, page: int = 0, number_of: int = 10):
        url = self._uri + self._exp_endpoint + "/list"
        params = {
            "num": number_of,
            "page": page,
        }
        with self._session() as session:
            resp = session.request("GET", url, params=params)
            if resp.status_code == 200:
                return [ExperimentsEntitry(**el) for el in resp.json()]


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


    def __enter__(self):
        self.session = self._session()
        return self

    def __exit__(self, *args):
        self.session.close()

    def close(self):
        self._session.close()