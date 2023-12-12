"""CorfuMV docstring.

This is CorfuMV client document string.
CorfuMV is model versioning framework that uses NoSQL database as storage.
Version 0.1.1.post1 provides only Mongo interface (pymongo driver).
"""
from .server import app
from corfumv.client import CorfuClient
from corfumv.utils import set_corfumv_server_uri

__version__ = "0.1.2.dev1"