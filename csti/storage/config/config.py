import os
import typing as t

from csti.storage import SaveLoadStorage
from csti.storage.exceptions import FieldIsEmpty


class Config(SaveLoadStorage):
    def __init__(self, path: str):
        super().__init__()
        self._path = path
        self._data = {}
        self._isLoaded = False

    @property
    def path(self) -> str:
        return self._path

    @t.override
    def _get(self, location: tuple[str, ...]) -> t.Any:
        cur = self._data
        *loc, fieldName = location

        for name in loc:
            cur = cur.get(name, None)
            if not isinstance(cur, dict):
                raise FieldIsEmpty(location)

        if fieldName not in cur:
            raise FieldIsEmpty(location)
        return cur.get(fieldName)

    @t.override
    def _set(self, location: tuple[str, ...], value: t.Any):
        *other, fieldName = location
        cur: dict = self._data

        for name in other:
            if name not in cur:
                cur[name] = {}
            cur = cur.get(name)  # type: ignore

        cur[fieldName] = value

    @t.override
    def create(self):
        if not os.path.exists(self.path):
            with open(self.path, "w"):
                pass

    @t.override
    def load(self, force: bool = False):
        if self._isLoaded and not force:
            return
        self._isLoaded = True
