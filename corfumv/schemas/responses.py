from pydantic import BaseModel


class CreationResponse(BaseModel):
    message: str
    object_id: str
    name: str


class UpdationResponse(BaseModel):
    message: str
    object_id: str
    update: str
    modefied_count: int


class DeletionResponse(BaseModel):
    message: str
    object_id: str
    deleted_count: int
