from pydantic import Field
from .models import Experiments, Models, ModelMetrics, ModelParams
from typing import Union
from corfumv.core import Entity
from .enums import UpdateExperiment


class ModelsEntity(Models, Entity):
    """Model entity for client section."""

    uri: str = Field(exclude=True)
    _prefix: str = "/models"


    def add_param(self,
                   parameter: Union[str, ModelParams] = None,
                   value: Union[str, int, float] = None):
        params = parameter.model_dump() if isinstance(parameter, ModelParams) else {
            "metric": parameter,
            "value": value
        }
        options = {
            "method": "PATCH",
            "params": {"model_id": self.id},
            "json": params
        }
        self._make_request(**options)


    def add_metric(self,
                   metric: Union[str, ModelMetrics] = None,
                   value: Union[str, int, float] = None):
        metrics = metric.model_dump() if isinstance(metric, ModelMetrics) else {
            "metric": metric,
            "value": value
        }
        options = {
            "method": "PATCH",
            "params": {"model_id": self.id},
            "json": metrics
        }
        return self._make_request(**options)


    def set_config(self):
        raise NotImplementedError()


    def set_weights(self):
        raise NotImplementedError()


class ExperimentsEntitry(Experiments, Entity):
    """Class for client interaction.
    
    Initialize, customize and dump models to CorfuMV server."""

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
