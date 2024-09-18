import os
import typing as t
import abc

from csti.data_storage import DataStorage
from csti.data_storage.exceptions import FieldIsEmpty


class FileStorage(DataStorage):
    @abc.abstractmethod
    def getPathByLocation(self, location: tuple[str, ...]) -> str:
        """ Получение пути файла. """
        pass

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
