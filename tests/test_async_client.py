import pytest
from tests.conftest import TEST_CORFUMV_URI
from corfumv.client import CorfuClient


@pytest.fixture(scope="module")
def async_client():
    pass