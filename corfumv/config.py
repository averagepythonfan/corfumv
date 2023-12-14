import os

SYNC: bool = bool(os.getenv("SYNC", True))
MONGO = os.getenv("MONGO", "mongodb://root:secret@172.17.0.2:27017")
REDIS = os.getenv("REDIS", None)
