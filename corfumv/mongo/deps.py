from CorfuMV.config import SYNC, MONGO
from pymongo import MongoClient
from .unit_of_work import PymongoUnitOfWork
from .service import PymongoCRUDService


client = MongoClient(MONGO, connect=False) 


def get_uow():
    return PymongoUnitOfWork(client=client) if SYNC else None # implement async uow


def get_service():
    return PymongoCRUDService(uow=get_uow()) if SYNC else None # implement async service
