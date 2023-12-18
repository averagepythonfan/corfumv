from typing import List, TypeVar, Union

from numpy import ndarray, float32
from pydantic import Field

from corfumv.core import Entity

from .enums import UpdateExperiment, UpdateModelBase
from .models import Experiments, ModelMetrics, ModelParams, Models

TFModelMock = TypeVar("TFModelMock")


class ModelsEntity(Models, Entity):
    """Model entity for client section."""

    uri: str = Field(exclude=True)
    _prefix: str = "/models"


    def add_param(self,
                   parameter: Union[str, ModelParams] = None,
                   value: Union[str, float] = None) -> dict:
        params = parameter.model_dump() if isinstance(parameter, ModelParams) else {
            "parameter": parameter,
            "value": value
        }
        options = {
            "method": "PATCH",
            "url": self.uri + self._prefix + self._set + "/params",
            "params": {"model_id": self.id},
            "json": params
        }
        return self._make_request(**options)


    def remove_params(self,
                      param_name: str):
        options = {
            "method": "DELETE",
            "url": self.uri + self._prefix + self._delete + "/params",
            "params": {
                "model_id": self.id,
                "param_name": param_name
            }
        }
        return self._make_request(**options)


    def add_metric(self,
                   metric: Union[str, ModelMetrics] = None,
                   value: Union[str, float] = None) -> dict:
        metrics = metric.model_dump() if isinstance(metric, ModelMetrics) else {
            "metric": metric,
            "value": value
        }
        options = {
            "method": "PATCH",
            "url": self.uri + self._prefix + self._set + "/metrics",
            "params": {"model_id": self.id},
            "json": metrics
        }
        return self._make_request(**options)


    def remove_metric(self,
                      metric_name: str) -> dict:
        options = {
            "method": "DELETE",
            "url": self.uri + self._prefix + self._delete + "/metrics",
            "params": {
                "model_id": self.id,
                "metric_name": metric_name
            }
        }
        return self._make_request(**options)


    def set_description(self, description: str) -> dict:
        return self._patch_request(
            update=UpdateModelBase.set_description.value,
            value=description
        )


    def set_config(self, config: dict) -> dict:
        if self.config:
            raise KeyError("Config is already initialized")
        options = {
            "method": "POST",
            "url": self.uri + self._prefix + self._set + "/config",
            "json": {
                "model_id": self.id,
                "config": config
            }
        }
        if response := self._make_request(**options):
            self.config = "Initialized"
            return response


    def set_weights(self, weights: List[dict]) -> dict:
        if self.weights:
            raise KeyError("Weights are already initialized")
        options = {
            "method": "POST",
            "url": self.uri + self._prefix + self._set + "/weights",
            "json": {
                "model_id": self.id,
                "weights": weights
            }
        }
        if response := self._make_request(**options):
            self.weights = "Initialized"
            return response


    def _fetch_config(self) -> dict:
        options = {
            "method": "GET",
            "url": self.uri + self._prefix + "/config",
            "params": {
                "model_id": self.id
            }
        }
        response = self._make_request(**options)
        return response["config"]


    def _fetch_weights(self) -> List[ndarray]:
        options = {
            "method": "GET",
            "url": self.uri + self._prefix + "/weights",
            "params": {
                "model_id": self.id
            }
        }
        response = self._make_request(**options)
        return [ndarray(el, dtype=float32) for el in response["weights"]]


    def fetch_model(self, sequential: TFModelMock) -> TFModelMock:
        seq = sequential.from_config(config=self._fetch_config())
        seq.set_weights(weights=self._fetch_weights())
        return seq


class ExperimentsEntitry(Experiments, Entity):
    """Class for client interaction.

    Initialize, customize and dump models to CorfuMV server.
    """

    uri: str = Field(exclude=True)
    _prefix: str = "/experiments"


    def add_model(self, model: Union[Models, ModelsEntity]):
        return self._patch_request(
            update=UpdateExperiment.add_model.value,
            value=model.id
        )


    def remove_model(self, model: Union[Models, ModelsEntity]):
        return self._patch_request(
            update=UpdateExperiment.remove_model.value,
            value=model.id
        )
