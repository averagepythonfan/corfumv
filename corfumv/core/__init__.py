"""Core package.

Provides `entity`, `repository`, `unit_of_work` and `service` classes.
"""
from .entity import Entity
from .repository import AsyncRepository, SyncRepository
from .service import SyncCRUDService
from .unit_of_work import AsyncUnitOfWork, SyncUnitOfWork
from .client import SyncClient, AsyncClient
