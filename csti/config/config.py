import typing as t

import yaml

from csti.data_storage import SaveLoadStorage
from csti.data_storage.exceptions import FieldIsEmpty, SaveError, LoadError


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


class YAMLConfig(Config):
    @t.override
    def save(self):
        try:
            with open(self.path, "w") as file:
                yaml.dump(self._data, file, allow_unicode=True, sort_keys=False)
        except OSError:
            raise SaveError(f"Не удалось сохранить данные в файл '{self.path}'.")

    @t.override
    def load(self):
        try:
            with open(self._path, "r") as file:
                self._data = yaml.safe_load(file)
        except OSError:
            raise LoadError(f"Не удалось загрузить данные из файла '{self.path}'.")
        except yaml.YAMLError as e:
            raise LoadError(f"Ошибка при загрузке файла '{self.path}': {e}")
    
    def create(self):
        with open(self.path, "w") as file:
            pass
