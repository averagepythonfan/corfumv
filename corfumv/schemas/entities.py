from typing import List, Union

from pydantic import Field

from corfumv.core import Entity

from .enums import UpdateExperiment, UpdateModelBase
from .models import Experiments, ModelMetrics, ModelParams, Models


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
        options = {
            "method": "POST",
            "url": self.uri + self._prefix + self._set + "/config",
            "json": {
                "model_id": self.id,
                "config": config
            }
        }
        return self._make_request(**options)


    def set_weights(self, weights: List[dict]) -> dict:
        options = {
            "method": "POST",
            "url": self.uri + self._prefix + self._set + "/weights",
            "json": {
                "model_id": self.id,
                "weights": weights
            }
        }
        return self._make_request(**options)


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
