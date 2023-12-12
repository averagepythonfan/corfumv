from dataclasses import dataclass
import datetime
# from pydantic import BaseModel
from typing import Optional, List, Union
from bson.objectid import ObjectId
from .tf_model import ModelEntity


@dataclass
class ExperimentEntity:
    _experiment_id: Optional[ObjectId] = None
    experiment_name: Optional[str] = None
    experiment_tags: Optional[Union[dict, str]] = None
    date: datetime.datetime = datetime.datetime.now()
    _models_list: Optional[List[ObjectId]] = None


    @property
    def id(self):
        return self._experiment_id


    @id.setter
    def id(self, uid: ObjectId):
        if isinstance(uid, ObjectId):
            self._experiment_id = uid
        else:
            TypeError(
                f"Model id must be BSON ObjectId type, not {type(uid)}"
            )

    @property
    def models_list(self):
        return self._models_list


    def add_model(self, model: Union[ObjectId, ModelEntity]):
        if isinstance(model, ObjectId):
            if self._models_list:
                self._models_list.append(model)
            else:
                self._models_list = [model]
        elif isinstance(model, ModelEntity):
            if model.id:
                self._models_list.append(model.id)
            else:
                raise KeyError("Models does not have an ID")
        else:
            raise TypeError(
                f"Model must be ObjectId or TFModelEntity type, not {type(model)}"
            )
    
    def export(self):
        raise NotImplementedError("Plase, implement experiment entity export")