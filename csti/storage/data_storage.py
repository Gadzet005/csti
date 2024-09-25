import abc
import typing as t

from csti.storage.exceptions import FieldIsEmpty, FieldValueError
from csti.storage.field import Field
from csti.storage.template import Group, StorageTemplate


class ReadOnlyStorage(abc.ABC):
    """Интерфейс для просмотра данных в хранилище."""

    template: StorageTemplate = StorageTemplate([])

    @abc.abstractmethod
    def _get(self, location: tuple[str, ...]) -> t.Any:
        """
        Получение значения без какой-либо обработки.
        Ошибка `FieldIsEmpty`, если значение не найдено.
        """
        pass

    @t.overload
    def get(self, *location: str) -> t.Any:
        """
        Получить значение из хранилища.
        - Ошибка `FieldIsEmpty`, если значение не найдено.
        - Ошибка `FieldValueError`, если поле имеет невалидное значение.

        :param location:
            Список названий полей, в которые данное поле вложено и название самого поля.
            Например, для user.info.name location=[user, info, name].
        """
        pass

    @t.overload
    def get(self, *location: str, default=None) -> t.Any:
        """
        Получить значение из хранилища.
        - Ошибка `FieldIsEmpty`, если значение не найдено.
        - Ошибка `FieldValueError`, если поле имеет невалидное значение.

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
            success, result = field.deserialize(rawValue)
            if not success:
                raise FieldValueError(location, rawValue)
            return result
        except FieldIsEmpty as error:
            hasDefault, default = field.default
            if hasDefault:
                return default
            elif "default" in kwargs:
                default = kwargs.pop("default")
                return default
            else:
                raise error

    def contains(self, *location: str) -> bool:
        """Проверить наличие данного поля в шаблоне и наличия у него значения."""

        # Проверка наличия в шаблоне.
        success, result = self.template.get(*location)
        if not success:
            return False

        if isinstance(result, Field):
            # Проверка наличия значения у поля
            try:
                self._get(location)
                return True
            except FieldIsEmpty:
                return False
        elif isinstance(result, Group):
            return True
        else:
            return False

    @t.overload
    def __getitem__(self, key: str): ...
    @t.overload
    def __getitem__(self, location: tuple[str, ...]): ...

    def __getitem__(self, *args, **kwargs):
        location = args[0]
        if isinstance(location, str):
            return self.get(location)
        else:
            return self.get(*location)

    @t.overload
    def __contains__(self, key: str): ...
    @t.overload
    def __contains__(self, location: tuple[str, ...]): ...

    def __contains__(self, *args, **kwargs):
        location = args[0]
        if isinstance(location, str):
            return self.contains(location)
        else:
            return self.contains(*location)


class DataStorage(ReadOnlyStorage):
    """Интерфейс для работы с хранилищем данных."""

    def create(self):
        """
        Создание хранилища. Например, создание файлов для хранения.
        Если хранилище уже создано, то ничего не изменяется.
        """
        pass

    @abc.abstractmethod
    def _set(self, location: tuple[str, ...], value: t.Any):
        """Выставление значения без какой-либо обработки."""
        pass

    def set(self, *location: str, value: t.Any):
        """
        По аналогии с `get`
        Ошибка `FieldValueError`, если `value` нельзя присвоить полю.
        """

        field = self.template.getField(*location)
        success, result = field.serialize(value)
        if not success:
            raise FieldValueError(location, value)
        self._set(location, result)

    @t.overload
    def __setitem__(self, key: str, value: t.Any): ...
    @t.overload
    def __setitem__(self, location: tuple[str, ...], value: t.Any): ...

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
        """
        Сохранить данные из экземпляра.
        Если не удалось, выкинет `SaveError`.
        """
        pass

    @abc.abstractmethod
    def load(self):
        """
        Загрузить данные в экземпляр.
        Если не удалось, выкинет `LoadError`.
        """
        pass
