from .models import Experiments, Models
from typing import Union
from corfumv.utils import get_corfumv_server_uri
from requests import Session
from corfumv.core import Entity
from .enums import UpdateExperiment, UpdateModel


class ModelsEntity(Models, Entity):
    _prefix: str = "/models"
    _uri: str = get_corfumv_server_uri

    def _patch_request(self, update: str, value: str) -> dict:
        options = {
            "method": "PATCH",
            "url": self._uri() + self._prefix + self._set ,
            "json": {
                'instance_id': self.id,
                'update': update,
                'value': value,
            }
        }
        with Session() as session:
            resp = session.request(**options)
            if resp.status_code == 200:
                return resp.json()
            else:
                raise ConnectionError(resp.text())


    def rename(self, new_name: str):
        return self._patch_request(
            update=UpdateModel.rename.value,
            value=new_name
        )


    def add_tag(self, tag: str):
        return self._patch_request(
            update=UpdateModel.add_tag.value,
            value=tag
        )


    def remove_tag(self, tag: str):
        return self._patch_request(
            update=UpdateModel.remove_tag.value,
            value=tag
        )


class ExperimentsEntitry(Experiments, Entity):
    """Class for client interaction.
    
    Initialize, customize and dump models to CorfuMV server."""

    _prefix: str = "/experiments"
    _uri: str = get_corfumv_server_uri

    def _patch_request(self, update: str, value: str) -> dict:
        options = {
            "method": "PATCH",
            "url": self._uri() + self._prefix + self._set ,
            "json": {
                'instance_id': self.id,
                'update': update,
                'value': value,
            }
        }
        with Session() as session:
            resp = session.request(**options)
            if resp.status_code == 200:
                return resp.json()
            else:
                raise ConnectionError(resp.text())


    def rename(self, new_name: str):
        return self._patch_request(
            update=UpdateExperiment.rename.value,
            value=new_name
        )


    def add_tag(self, tag: str):
        return self._patch_request(
            update=UpdateExperiment.add_tag.value,
            value=tag
        )


    def remove_tag(self, tag: str):
        return self._patch_request(
            update=UpdateExperiment.remove_tag.value,
            value=tag
        )

    def add_model(self, model: Union[Models, ModelsEntity]):
        return self._patch_request(
            update=UpdateExperiment.add_tag.value,
            value=model.id
        )


    def remove_model(self, model: Union[Models, ModelsEntity]):
        return self._patch_request(
            update=UpdateExperiment.remove_tag.value,
            value=model.id
        )
