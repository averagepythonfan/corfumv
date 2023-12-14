import os
from typing import Optional


def set_corfumv_server_uri(uri: str) -> None:
    """Set `uri` in environment."""
    if isinstance(uri, str):
        os.environ["CORFUMV_URI"] = uri
    else:
        raise TypeError(f"`uri` must be `str` type, not {type(uri)}")


def get_corfumv_server_uri() -> Optional[str]:
    """Get `uri` from environment."""
    uri = os.environ.get("CORFUMV_URI")
    if uri:
        return uri
    else:
        raise ConnectionError("`CORFUMV_URI` is not set")
