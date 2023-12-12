import datetime
from dataclasses import dataclass
from typing import Optional, List, Union
from bson.objectid import ObjectId


@dataclass
class ModelEntity:
    _model_id: Optional[ObjectId] = None
    _model_params: Optional[dict] = None
    model_name: Optional[str] = None
    model_tags: Optional[Union[dict, str]] = None
    _metrics: Optional[dict] = None
    description: Optional[str] = None
    date: datetime.datetime = datetime.datetime.now()
    _config: Optional[dict] = None
    _weights: Optional[List[List]] = None


    @property
    def id(self):
        return self._model_id

    @id.setter
    def id(self, uid: ObjectId):
        """Accepts a unique id from Mongo database.
        Must set after insertion automatically."""

        if isinstance(uid, ObjectId):
            self._model_id = uid
        else:
            TypeError(
                f"Model id must be BSON ObjectId type, not {type(uid)}"
            )


    @property
    def model_params(self):
        return self._model_params


    def add_params(self, params: dict):
        """Accepts a dict with model parameters.
        It might be random seed, batch size,
        hyperparameters, etc.
        
        :Parameters:
            - `params`: a dict type instance.
                        If it's not a dict, throws a TypeError.
        
        >>> md = TFModelEntity()
        >>> params = {'random_seed': 801, 'batch_size': 50}
        >>> md.add_params(params)"""

        if isinstance(params, dict):
            if self._model_params is None:
                self._model_params = params
            else:
                self._model_params.update(params)
        else:
            raise TypeError(
                f"Model params must be Dict, not {type(params)}"
            )


    @property
    def metrics(self):
        return self._metrics

    def add_metrics(self, metrics: dict):
        """Accepts a dict with metrics.
        It might be accuracy, F1-score, etc.
        
        :Parameters:
            - `params`: a dict type instance.
                        If it's not a dict, throws a TypeError.
        
        >>> md = TFModelEntity()
        >>> metrics = {'accuracy': 0.58, 'f1-score': 0.52}
        >>> md.add_metrics(metrics)"""

        if isinstance(metrics, dict):
            if self._metrics is None:
                self._metrics = metrics
            else:
                self._metrics.update(metrics)
        else:
            raise TypeError(
                f"Model params must be Dict, not {type(metrics)}"
            )

    
    # @property
    # def model_config(self):
    #     return self._config

    # @model_config.setter
    # def model_config(self, config: dict):
    #     if isinstance(config, dict):
    #         self._config = config
    #     else:
    #         raise TypeError(f"Config must be dict, not {type(config)}")


    # @property
    # def model_weights(self):
    #     return self._weights

    # @model_weights.setter
    # def model_weights(self, weights: List[numpy.ndarray]):
    #     if isinstance(weights, list):
    #         if (
    #             all(isinstance(el, numpy.ndarray) for el in weights)
    #             or
    #             all(isinstance(el, list) for el in weights)
    #         ):
    #             self._weights = weights
    #         else:
    #             raise TypeError("Weight must be List of Numpy Arrays")
    #     else:
    #         raise TypeError(
    #             f"Weights must be List of Numpy Arrays, not {type(weights)}"
    #         )


    # def to_dict(self):
    #     """Shows an available model entity parameters.
    #     Do now show config and weights, only its status:
    #     `initialized` or `not initialized`."""

    #     data = dict()
    #     if self._model_id:
    #         data["model_id"] = self._model_id
    #     if self._model_params:
    #         data["model_params"] = self._model_params
    #     if self.model_name:
    #         data["model_name"] = self.model_name
    #     if self.model_tags:
    #         data["model_tags"] = self.model_tags
    #     if self._metrics:
    #         data["metrics"] = self._metrics
    #     if self.description:
    #         data["description"] = self.description
    #     if self.date:
    #         data["date"] = self.date
    #     if self._config:
    #         data["config"] = 'initialized'
    #     else:
    #         data["config"] = 'not initialized'
    #     if self._weights:
    #         data["weights"] = 'initialized'
    #     else:
    #         data["weights"] = 'not initialized'
    #     return data


    # def export(self):
    #     """Extract a full data of model entity.
    #     Pass to the interface of database."""

    #     data = self.to_dict()
    #     if (
    #         data['config'] == 'initialized'
    #         and
    #         data['weights'] == 'initialized'
    #     ):
    #         data['config'] = self._config
    #         data["weights"] = [el.tolist() for el in self._weights]
    #         return data
    #     else:
    #         raise KeyError(
    #             """Config or Weights are not uncluded,
    #             you can not export your model now"""
    #         )
