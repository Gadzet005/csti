import abc
import typing as t

from csti.data_storage.exceptions import FieldNotInitialized
from csti.data_storage.template import StorageTemplate


class DataStorage(abc.ABC):
    """Интерфейс для работы с хранилищем данных."""

    template: StorageTemplate = StorageTemplate([])

    @abc.abstractmethod
    def create(self):
        """
        Создание хранилища. Например, создание файлов для хранения.
        Если хранилище уже создано, то ничего не происходит.
        """
        pass

    @abc.abstractmethod
    def _get(self, location: tuple[str, ...]) -> t.Any:
        """
        Получение значения без какой-либо обработки.
        Ошибка FieldNotInitialized, если значение не найдено.
        """
        pass

    @abc.abstractmethod
    def _set(self, location: tuple[str, ...], value: t.Any):
        """Выставление значения без какой-либо обработки."""
        pass

    @t.overload
    def get(self, *location: str) -> t.Any:
        """
        Получить значение из хранилища.

        :param location:
            Список названий полей, в которые данное поле вложено и название самого поля.
            Например, для user.info.name location=[user, info, name].
        """
        pass

    @t.overload
    def get(self, *location: str, default=None) -> t.Any:
        """
        Получить значение из хранилища.

        :param location:
            Список названий полей, в которые данное поле вложено и название самого поля.
            Например, для user.info.name location=[user, info, name].
        :param default:
            Значение, которое будет возвращено, если поле не найдено и
            не установлено базовое значение по умолчанию.
        """
        pass

    def get(self, *location: str, **kwargs) -> t.Any:
        field = self.template.getField(*location)

        try:
            rawValue = self._get(location)
            return field.deserialize(rawValue)
        except FieldNotInitialized as error:
            if field.defaultValue is not None:
                return field.defaultValue
            elif "default" in kwargs:
                default = kwargs.pop("default")
                return default
            else:
                raise error

    def contains(self, *location: str) -> bool:
        """Проверить наличие данного поля."""
        try:
            self._get(location)
            return True
        except FieldNotInitialized:
            return False

    def set(self, *location: str, value: t.Any):
        """По аналогии с :func:`get`"""

        field = self.template.getField(*location)
        self._set(location, field.serialize(value))

    @t.overload
    def __getitem__(self, key: str):
        pass
    
    @t.overload
    def __getitem__(self, location: tuple[str,...]):
        pass

    def __getitem__(self, *args, **kwargs):
        location = args[0]
        if isinstance(location, str):
            return self.get(location)
        else:
            return self.get(*location)
    
    @t.overload
    def __setitem__(self, key: str, value: t.Any):
        pass
    
    @t.overload
    def __setitem__(self, location: tuple[str,...], value: t.Any):
        pass

    def __setitem__(self, *args, **kwargs):
        location, value = args
        if isinstance(location, str):
            return self.set(location, value=value)
        else:
            return self.set(*location, value=value)


class SaveLoadStorage(DataStorage):
    """
    Интерфейс для работы с хранилищем,
    которое предполагает загрузку и сохранение данных.
    """

    @abc.abstractmethod
    def save(self):
        """Сохранить данные из экземпляра."""
        pass

    @abc.abstractmethod
    def load(self):
        """Загрузить данные в экземпляр."""
        pass
