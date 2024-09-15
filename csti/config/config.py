import typing as t

import yaml

from csti.data_storage import SaveLoadStorage
from csti.data_storage.exceptions import FieldNotInitialized


class Config(SaveLoadStorage):
    def __init__(self, path: str):
        super().__init__()
        self._path = path
        self._data = {}

    @property
    def path(self) -> str:
        return self._path

    @t.override
    def _get(self, location: list[str]) -> t.Any:
        cur = self._data

        for name in location:
            cur = cur.get(name, None)
            if cur is None:
                raise FieldNotInitialized(location)

        return cur

    @t.override
    def _set(self, location: list[str], value: t.Any):
        fieldName = location.pop()
        cur: dict = self._data

        for name in location:
            if name not in cur:
                cur[name] = {}
            cur = cur.get(name)  # type: ignore

        cur[fieldName] = value


class YAMLConfig(Config):
    @t.override
    def save(self):
        with open(self.path, "w") as file:
            yaml.dump(self._data, file, allow_unicode=True, sort_keys=False)

    @t.override
    def load(self):
        with open(self._path, "r") as file:
            self._data = yaml.safe_load(file)
