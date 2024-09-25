import os
import typing as t

from csti.storage import DataStorage
from csti.storage.exceptions import FieldIsEmpty


class FileStorage(DataStorage):
    def __init__(self, dir: str):
        super().__init__()
        self._dir = dir

    @property
    def dir(self) -> str:
        return self._dir

    def getPathByLocation(self, location: tuple[str, ...]) -> str:
        return os.path.join(self.dir, *location)

    @t.override
    def _get(self, location: tuple[str, ...]) -> t.Any:
        try:
            with open(self.getPathByLocation(location), "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            raise FieldIsEmpty(location)

    @t.override
    def _set(self, location: tuple[str, ...], value):
        path = self.getPathByLocation(location)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(value)

    def create(self):
        os.makedirs(self.dir, exist_ok=True)
