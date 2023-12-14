from pymongo import MongoClient
from pymongo.client_session import ClientSession

from corfumv.core import SyncUnitOfWork

from .repository import SyncExperimentRepository, SyncModelRepository


class PymongoUnitOfWork(SyncUnitOfWork):

    def __init__(self,
                 client: MongoClient,
                 autocommit: bool = False) -> None:
        super(PymongoUnitOfWork, self).__init__(
            autocommit=autocommit
        )
        self.client = client

    def begin(self):
        self.session: ClientSession = self.client.start_session()

        self.experiment = SyncExperimentRepository(session=self.session)
        self.model = SyncModelRepository(session=self.session)

    def commit(self):
        pass

    def rollback(self):
        pass

    def close(self):
        self.session.end_session()
