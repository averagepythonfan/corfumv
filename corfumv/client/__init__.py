"""Client module.

It has `CorfuClient` and `CorfuAsyncClient` instances.
"""


# from .client import CorfuClient
from .async_client import HTTPXClient as CorfuAsyncClient
from .sync_clients import RequestsClient as CorfuClient
