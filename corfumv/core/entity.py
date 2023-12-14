from abc import ABC
from typing import Optional, Type

from requests import Session


class Entity(ABC):
    """Abstract entity class for experiments and models.

    Require a `rename` realization method, and `_prefix` property.
    Class implements `rename`, `add_tag`, `remove_tag` and `delete` method.
    """

    uri: str
    _prefix: str
    _create: str = "/create"
    _list: str = "/list"
    _find_by: str = "/find_by"
    _set: str = "/set"
    _delete: str = "/delete"
    _session: Type[Session] = Session


    def _make_request(self, **options: dict) -> Optional[dict]:
        """Private method to make requests with `Session` class."""
        with self._session() as session:
            resp = session.request(**options)
            if resp.status_code == 200:
                return resp.json()
            else:
                raise ConnectionError(resp.text)


    def _patch_request(self, update: str, value: str) -> dict:
        """Private `PATCH` method to make request to CorfuMV server."""
        options = {
            "method": "PATCH",
            "url": self.uri + self._prefix + self._set ,
            "params": {
                "instance_id": self.id,
                "update": update,
                "value": value,
            }
        }
        return self._make_request(**options)


    def rename(self, new_name: str) -> dict:
        """Rename any instance with private patch method."""
        return self._patch_request(
            update="rename",
            value=new_name
        )


    def add_tag(self, tag: str) -> dict:
        """Add tag to instance with private patch method."""
        return self._patch_request(update="add_tag", value=tag)


    def remove_tag(self, tag: str) -> dict:
        """Remove tag from instance with private patch method."""
        return self._patch_request(update="remove_tag", value=tag)


    def delete(self) -> dict:
        """Delete instance from db."""
        options = {
            "method": "DELETE",
            "url": self.uri + self._prefix + self._delete,
            "params": {
                "instance_id": self.id,
            }
        }
        return self._make_request(**options)
