from typing import Type

from pymongo.client_session import ClientSession
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from corfumv.core import SyncRepository
from corfumv.schemas import Experiments, MetaCollection, Models


class PymongoRepository(SyncRepository):

    model: Type[MetaCollection] = None

    def __init__(self,
                 session: ClientSession,
                 database: str = "corfudb") -> None:
        self.session = session
        self.client = self.session.client
        self.database: Database  = self.client.get_database(database)
        self.__coll: Collection = self.database.get_collection(
            self.model.Collection.name
        )


    def save(self,
             obj: Type[MetaCollection] = None,
             **obj_kwargs) -> bool:

        md: MetaCollection = obj if obj else self.model(**obj_kwargs)

        resp: InsertOneResult = self.__coll.insert_one(
            document=md.model_dump(exclude_none=True, by_alias=True),
            session=self.session
        )
        return resp.acknowledged


    def get(self,
            filter: dict = {},
            projection: dict = {}) -> Cursor[Type[MetaCollection]]:
        return self.__coll.find(
            filter=filter,
            projection=projection,
            session=self.session
        )


    def update(self,
               filter: dict = {},
               update: dict = {}) -> UpdateResult:
        return self.__coll.update_one(
            filter=filter,
            update=update,
            session=self.session
        )


    def delete(self, filter: dict) -> DeleteResult:
        return self.__coll.delete_one(
            filter=filter,
            session=self.session
        )


class SyncExperimentRepository(PymongoRepository):
    model = Experiments


class SyncModelRepository(PymongoRepository):
    model = Models
