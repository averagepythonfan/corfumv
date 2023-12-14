from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Request

from corfumv.core import SyncCRUDService
from corfumv.mongo import get_service
from corfumv.schemas import (
    FindBy,
    Instance,
    ModelMetrics,
    ModelParams,
    Models,
    UpdateModel,
    UpdateModelBase,
)

model_instance = Instance.model


router = APIRouter(
    prefix="/models",
    tags=["Models service"]
)


@router.post("/create")
async def create_model(
    md: Models,
    service: Annotated[SyncCRUDService, Depends(get_service)]
):
    """Create model by Models shcema"""
    return service.create(obj=md)


@router.get("/find_by")
async def find_model_by(
    service: Annotated[SyncCRUDService, Depends(get_service)],
    find_by: FindBy,
    value: Optional[str] = None,
    is_list: bool = False
):
    return service.read(
        instance=model_instance,
        find_by=find_by,
        value=value,
        is_list=is_list
    )


@router.get("/list")
async def get_model_list(
    service: Annotated[SyncCRUDService, Depends(get_service)],
    num: int = 10,
    page: int = 0
):
    resp = service.read(
        instance=model_instance,
        is_list=True
    )
    return resp[num*page:num*(page+1)]


@router.patch("/set")
async def set_model_metadata(
    service: Annotated[SyncCRUDService, Depends(get_service)],
    instance_id: str,
    update: UpdateModelBase,
    value: str
):
    return service.update(
        instance=model_instance,
        instance_id=instance_id,
        update=update,
        value=value
    )


@router.patch("/set/params")
async def set_model_params(
    service: Annotated[SyncCRUDService, Depends(get_service)],
    model_id: str,
    params: ModelParams
):
    return service.update(
        instance=model_instance,
        instance_id=model_id,
        update=UpdateModel.add_params,
        value=params.model_dump()
    )


@router.patch("/set/metrics")
async def set_model_metrics(
    service: Annotated[SyncCRUDService, Depends(get_service)],
    model_id: str,
    metrics: ModelMetrics
):
    return service.update(
        instance=model_instance,
        instance_id=model_id,
        update=UpdateModel.add_metric,
        value=metrics.model_dump()
    )


@router.post("/set/config")
async def insert_config(
    config: Request,
    service: Annotated[SyncCRUDService, Depends(get_service)]
):

    config = await config.json()

    try:
        model_id = config["model_id"]
        config = config["config"]
    except KeyError as e:
        raise HTTPException(
            status_code=441,
            detail=str(e)
        )

    return service.update(
        instance=model_instance,
        instance_id=model_id,
        update=UpdateModel.set_config,
        value=config
    )


@router.post("/set/weights")
async def insert_weights(
    weights: Request,
    service: Annotated[SyncCRUDService, Depends(get_service)]
):

    weights = await weights.json()

    try:
        model_id = weights["model_id"]
        weights = weights["weights"]
    except KeyError as e:
        raise HTTPException(
            status_code=441,
            detail=str(e)
        )

    return service.update(
        instance=model_instance,
        instance_id=model_id,
        update=UpdateModel.set_weights,
        value=weights
    )


@router.delete("/delete/params")
async def set_model_params(
    service: Annotated[SyncCRUDService, Depends(get_service)],
    model_id: str,
    param_name: str
):
    return service.update(
        instance=model_instance,
        instance_id=model_id,
        update=UpdateModel.remove_params,
        value=param_name
    )


@router.delete("/delete/metrics")
async def set_model_params(
    service: Annotated[SyncCRUDService, Depends(get_service)],
    model_id: str,
    metric_name: str
):
    return service.update(
        instance=model_instance,
        instance_id=model_id,
        update=UpdateModel.remove_metric,
        value=metric_name
    )


@router.delete("/delete")
async def delete_model_by_id(
    service: Annotated[SyncCRUDService, Depends(get_service)],
    instance_id: str
):
    """Delete experiment by its ID"""
    return service.delete(instance=model_instance, instance_id=instance_id)
