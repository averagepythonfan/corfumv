from typing import Annotated, Optional
from fastapi import APIRouter, Depends
from CorfuMV.schemas import Experiments, Instance, FindBy, UpdateExperiment
from CorfuMV.core import SyncCRUDService
from CorfuMV.mongo import get_service


experiment_instance = Instance.experiment


router = APIRouter(
    prefix="/experiments",
    tags=["Experiments service"]
)


@router.post("/create")
async def create_experiment(
    exp: Experiments,
    service: Annotated[SyncCRUDService, Depends(get_service)]
    
):
    """Create an experiment by Experiments using CRUD service.
    Return a CreationResponse, or raise HTTP exception"""

    return service.create(obj=exp)


@router.get("/list")
async def get_experiment_list(
    service: Annotated[SyncCRUDService, Depends(get_service)],
    num: int = 10,
    page: int = 0
):
    resp = service.read(
        instance=experiment_instance,
        is_list=True
    )
    return resp[num*page:num*(page+1)]


@router.get("/find_by")
async def find_experiment_by(
    service: Annotated[SyncCRUDService, Depends(get_service)],
    find_by: FindBy,
    value: Optional[str] = None,
    is_list: bool = False,
):
    """Find experiment by params."""

    return service.read(
        instance=experiment_instance,
        find_by=find_by,
        value=value,
        is_list=is_list
    )


@router.patch("/set")
async def set_params(
    service: Annotated[SyncCRUDService, Depends(get_service)],
    instance_id: str,
    update: UpdateExperiment,
    value: str
):
    """Update properties for experiment instance.
    
    You might rename model, add and remove tags or models."""
    return service.update(
        instance=experiment_instance,
        instance_id=instance_id,
        update=update,
        value=value
    )


@router.delete("/delete")
async def delete_by_id(
    service: Annotated[SyncCRUDService, Depends(get_service)],
    instance_id: str
):
    """Delete experiment by its ID"""
    return service.delete(instance=experiment_instance, instance_id=instance_id)
