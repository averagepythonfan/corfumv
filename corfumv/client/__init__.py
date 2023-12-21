"""Client module.

It has only `CorfuClient` instance.
"""


# from .client import CorfuClient
from .async_client import HTTPXClient as CorfuAsyncClient
from .sync_clients import RequestsClient as CorfuClient
