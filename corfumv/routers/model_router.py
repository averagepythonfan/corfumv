from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request

from corfumv.core import SyncCRUDService
from corfumv.mongo import get_service
from corfumv.schemas import (
    CreationResponse,
    DeletionResponse,
    FindBy,
    Instance,
    ModelMetrics,
    ModelParams,
    Models,
    UpdateModel,
    UpdateModelBase,
    UpdationResponse,
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
) -> CreationResponse:
    """Create model by Models shcema."""

    return service.create(obj=md)


@router.get("/find_by")
async def find_model_by(
    service: Annotated[SyncCRUDService, Depends(get_service)],
    find_by: FindBy,
    value: Optional[str] = None,
    is_list: bool = False
) -> list:
    """Find models by params. Might be a list of several models,
    if `is_list` is `True`.
    """
    resp: List[Models] = service.read(
        instance=model_instance,
        find_by=find_by,
        value=value,
        is_list=is_list
    )
    return [el.model_dump(exclude=["config", "weights"], by_alias=True) for el in resp]


@router.get("/list")
async def get_model_list(
    service: Annotated[SyncCRUDService, Depends(get_service)],
    num: int = 10,
    page: int = 0
) -> list:
    """Return list of existing models."""

    resp: List[Models] = service.read(
        instance=model_instance,
        is_list=True
    )
    return [
        el.model_dump(
            exclude=["config", "weights"],
            by_alias=True
        ) for el in resp[num*page:num*(page+1)]
    ]


@router.patch("/set")
async def set_model_metadata(
    service: Annotated[SyncCRUDService, Depends(get_service)],
    instance_id: str,
    update: UpdateModelBase,
    value: str
) -> UpdationResponse:
    """Set `name`, `tags` and `description` of model."""

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
) -> UpdationResponse:
    """Set model's `params`."""

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
) -> UpdationResponse:
    """Set model's `metrics`."""

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
)-> UpdationResponse:
    """Set model's `config`."""

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
) -> UpdationResponse:
    """Set model's `weights`."""

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


@router.get("/config")
async def get_model_config(
    service: Annotated[SyncCRUDService, Depends(get_service)],
    model_id: str,
) -> dict:
    resp: List[Models] = service.read(
        instance=model_instance,
        find_by=FindBy.id,
        value=model_id,
    )
    md = resp[0]
    return {"config": md.config}


@router.get("/weights")
async def get_model_weights(
    service: Annotated[SyncCRUDService, Depends(get_service)],
    model_id: str,
) -> dict:
    resp: List[Models] = service.read(
        instance=model_instance,
        find_by=FindBy.id,
        value=model_id,
    )
    md = resp[0]
    return {"weights": md.weights}


@router.delete("/delete/params")
async def delete_model_params(
    service: Annotated[SyncCRUDService, Depends(get_service)],
    model_id: str,
    param_name: str
) -> UpdationResponse:

    return service.update(
        instance=model_instance,
        instance_id=model_id,
        update=UpdateModel.remove_params,
        value=param_name
    )


@router.delete("/delete/metrics")
async def delete_model_metrics(
    service: Annotated[SyncCRUDService, Depends(get_service)],
    model_id: str,
    metric_name: str
) -> UpdationResponse:

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
) -> DeletionResponse:
    """Delete experiment by its ID"""

    return service.delete(
        instance=model_instance,
        instance_id=instance_id
    )
