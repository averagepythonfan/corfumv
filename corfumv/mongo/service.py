import logging
from datetime import datetime
from typing import List, Optional, Union
from pymongo.results import UpdateResult, DeleteResult
from fastapi import HTTPException
from corfumv.core import SyncCRUDService
from .unit_of_work import PymongoUnitOfWork
from corfumv.schemas import (Experiments,
                             Models,
                             CreationResponse,
                             UpdationResponse,
                             DeletionResponse,
                             Instance, 
                             FindBy,
                             UpdateExperiment,
                             UpdateModel,
                             ModelMetrics,
                             ModelParams)
from .misc import validate_cursor, query, update_query


AnyObject = Union[Experiments, Models]


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("pymongo.service.crud")


class PymongoCRUDService(SyncCRUDService):
    """Pymongo CRUD service.
    
    Require a UOW instance.
    Uses only in endpoints, might raise HTTP exceptions."""

    def __init__(self, uow: PymongoUnitOfWork) -> None:
        self.uow = uow


    def create(self, obj: AnyObject) -> Optional[CreationResponse]:
        if isinstance(obj, Experiments):
            with self.uow:
                if self.uow.experiment.save(obj=obj):
                    logger.info(f"experiment created, id: {obj.id}")
                    return CreationResponse(
                        message="experiment created successfully",
                        object_id=obj.id,
                        name=obj.name
                    )
                else:
                    logger.error(f"experiment not created, id: {obj.id}")
                    raise HTTPException(
                        status_code=432,
                        detail="fail due creation experiment"
                    )
        elif isinstance(obj, Models):
            with self.uow:
                if self.uow.model.save(obj=obj):
                    logger.info(f"model created, id: {obj.id}")
                    return CreationResponse(
                        message="model created successfully",
                        object_id=obj.id,
                        name=obj.name
                    )
                else:
                    logger.error(f"model not created, id: {obj.id}")
                    raise HTTPException(
                        status_code=433,
                        detail="fail due creation model"
                    )
        else:
            logger.error("CREATE: unknown instance")
            raise HTTPException(
                status_code=434,
                detail="unknown instance"
            )
    

    def read(self,
             instance: Instance,
             find_by: FindBy = None,
             value: Union[str, datetime, List[str]] = None,
             is_list: bool = False) -> Optional[List[AnyObject]]:
        """Find object by params"""

        params = {
            "find_by": find_by,
            "value": value
        }

        q = query(**params)

        if instance is Instance.experiment:
            with self.uow:
                cur = self.uow.experiment.get(filter=q if find_by and value else {})
                validated: list | str = validate_cursor(cur=cur, is_list=is_list)
                if isinstance(validated, list):
                    logger.info(f"read experiments, lenght: {len(validated)}")
                    return validated
                
                else:
                    logger.warning("read experiments are not validated")
                    raise HTTPException(
                        status_code=435,
                        detail={
                            "message": "read failed",
                            "detail": validated 
                        }
                    )

        elif instance is Instance.model:
            with self.uow:
                cur = self.uow.model.get(filter=q if find_by else {})
                validated: list | str = validate_cursor(cur=cur, is_list=is_list)
                if isinstance(validated, list):
                    logger.info(f"read models, lenght: {len(validated)}")
                    return validated

                else:
                    logger.warning("read models are not validated")
                    raise HTTPException(
                        status_code=435,
                        detail={
                            "message": "read failed",
                            "detail": validated 
                        }
                    )

        else:
            logger.error("READ: unknown instance")
            raise HTTPException(
                status_code=434,
                detail="unknown instance"
            )


    def update(self,
               instance: Instance,
               instance_id: str,
               update: Union[UpdateExperiment, UpdateModel],
               value: Union[str, ModelParams, ModelMetrics]) -> Optional[UpdationResponse]:
        """Update instance by its ID."""

        if instance is Instance.experiment:
            if update is UpdateExperiment.add_model:
                with self.uow:
                    cur = self.uow.experiment.get({"_id": value})
                    if len(list(cur)) == 0:
                        raise HTTPException(
                            status_code=435,
                            detail="model not found"
                        )
            q = update_query(update=update, value=value)
            with self.uow:
                result: UpdateResult = self.uow.experiment.update(
                    filter={"_id": instance_id},
                    update=q
                )
                mod_count = result.modified_count
                if mod_count != 0:
                    logger.info(f"experiment successfully updated, id: {instance_id}")
                    return UpdationResponse(
                        message="experiment successfully updated",
                        object_id=instance_id,
                        update=update.value,
                        modefied_count=mod_count
                    )

                else:
                    logger.warning(f"experiment update failed, id: {instance_id}")
                    raise HTTPException(
                        status_code=436,
                        detail="Modified count is 0"
                    )

        elif instance is Instance.model:
            q = update_query(update=update, value=value)
            with self.uow:
                result: UpdateResult = self.uow.model.update(
                    filter={"_id": instance_id},
                    update=q
                )
                mod_count = result.modified_count
                if mod_count != 0:
                    logger.info(f"model successfully updated, id: {instance_id}")
                    return UpdationResponse(
                        message="model successfully updated",
                        object_id=instance_id,
                        update=update.value,
                        modefied_count=mod_count
                    )

                else:
                    logger.warning(f"model update failed, id: {instance_id}")
                    raise HTTPException(
                        status_code=436,
                        detail="Modified count is 0"
                    )
        else:
            logger.error("UPDATE: unknown instance")
            raise HTTPException(
                status_code=434,
                detail="unknown instance"
            )


    def delete(self,
               instance: Instance,
               instance_id: str) -> Optional[DeleteResult]:
        """Delete instance by its ID"""
        f = {"_id": instance_id}
        if instance is Instance.experiment:
            with self.uow:
                response: DeleteResult = self.uow.experiment.delete(
                    filter=f
                )
                if response.acknowledged:
                    logger.info(f"experiment deleted, id: {instance_id}")
                    return DeletionResponse(
                        message="experiment deleted",
                        object_id=instance_id,
                        deleted_count=response.deleted_count
                    )

                else:
                    logger.warning(f"experiment did not deleted, id: {instance_id}")
                    raise HTTPException(
                        status_code=437,
                        detail="Deleted cound is 0"
                    )

        elif instance is Instance.model:
            with self.uow:
                response: DeleteResult = self.uow.model.delete(
                    filter=f
                )
                if response.acknowledged:
                    logger.info(f"model deleted, id: {instance_id}")
                    return DeletionResponse(
                        message="model deleted",
                        object_id=instance_id,
                        deleted_count=response.deleted_count
                    )

                else:
                    logger.warning(f"model did not deleted, id: {instance_id}")
                    raise HTTPException(
                        status_code=437,
                        detail="Deleted cound is 0"
                    )
        else:
            logger.error("DELETE: unknown instance")
            raise HTTPException(
                status_code=434,
                detail="unknown instance"
            )
