from fastapi.testclient import TestClient
from pymongo import MongoClient
from corfumv import app
from corfumv.mongo import get_service, PymongoUnitOfWork, PymongoCRUDService


def pymongo_client_service():
    TEST_MONGO_URI = "mongodb://test:test@localhost:27017"
    test_mongo = MongoClient(TEST_MONGO_URI)

    def override_get_service():
        return PymongoCRUDService(uow=PymongoUnitOfWork(client=test_mongo))

    app.dependency_overrides[get_service] = override_get_service
    return TestClient(app=app)
