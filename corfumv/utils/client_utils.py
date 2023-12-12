import os


def set_corfumv_server_uri(uri: str):
    if isinstance(uri, str):
        os.environ["CORFUMV_URI"] = uri
    else:
        raise TypeError(f"`uri` must be `str` type, not {type(uri)}")


def get_corfumv_server_uri():
    uri = os.environ.get("CORFUMV_URI")
    if uri:
        return uri
    else:
        pass
        # raise ConnectionError("`CORFUMV_URI` is not set")
