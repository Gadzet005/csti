import typing as t

from csti.data_storage import SaveLoadStorage
from csti.data_storage.exceptions import FieldIsEmpty


class Config(SaveLoadStorage):
    def __init__(self, path: str):
        super().__init__()
        self._path = path
        self._data = {}

    @property
    def path(self) -> str:
        return self._path

    @t.override
    def _get(self, location: tuple[str, ...]) -> t.Any:
        cur = self._data

        for name in location:
            cur = cur.get(name, None)
            if cur is None:
                raise FieldIsEmpty(location)

        return cur

    @t.override
    def _set(self, location: tuple[str, ...], value: t.Any):
        *other, fieldName = location
        cur: dict = self._data

        for name in other:
            if name not in cur:
                cur[name] = {}
            cur = cur.get(name)  # type: ignore

        cur[fieldName] = value
