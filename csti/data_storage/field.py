import abc
import typing as t
from enum import Enum

from csti.data_storage.template_element import TemplateElement


class Field(abc.ABC, TemplateElement):
    """Базовый класс поля в хранилище."""

    # Может быть переопределено в наследниках.
    # Тип для хранения.
    RAW = t.Any
    # Тип для использования.
    COMMON = t.Any

    @t.overload
    def __init__(self, name: str): ...
    @t.overload
    def __init__(self, name: str, *, default: COMMON): ...

    def __init__(self, name: str, **kwargs):
        super().__init__(name)

        self._hasDefault = "default" in kwargs
        self._default = kwargs.pop("default", None)

    @property
    def default(self) -> tuple[bool, COMMON]:
        """
        Кортеж из двух элементов: имеется ли значение
        по умолчанию и значение по умолчанию или `None`
        """
        return self._hasDefault, self._default

    @abc.abstractmethod
    def serialize(self, value: COMMON) -> tuple[bool, t.Optional[RAW]]:
        """
        Объект для использования -> объект для хранения.
        Возвращает кортеж из двух элементов:
        успех/неудача и преобразованный объект/`None`.
        """
        pass

    @abc.abstractmethod
    def deserialize(self, value: RAW) -> tuple[bool, t.Optional[COMMON]]:
        """
        Объект для хранения -> объект для использования.
        Возвращает кортеж из двух элементов:
        успех/неудача и преобразованный объект/`None`.
        """
        pass


class TypeField(Field):
    RAW = type
    COMMON = type

    @t.override
    def serialize(self, value: COMMON) -> tuple[bool, t.Optional[RAW]]:
        if not isinstance(value, self.COMMON):
            return False, None
        try:
            return True, self.RAW(value)
        except ValueError:
            return False, None

    @t.override
    def deserialize(self, value: RAW) -> tuple[bool, t.Optional[COMMON]]:
        if not isinstance(value, self.RAW):
            return False, None
        try:
            return True, self.COMMON(value)
        except ValueError:
            return False, None


class StringField(TypeField):
    RAW = str
    COMMON = str


class EnumField(Field):
    RAW = str
    COMMON = Enum

    @t.overload
    def __init__(self, name: str, enumType: t.Type[Enum]): ...
    @t.overload
    def __init__(self, name: str, enumType: t.Type[Enum], *, default: COMMON): ...

    def __init__(self, name: str, enumType: t.Type[Enum], **kwargs):
        super().__init__(name, **kwargs)
        self._enumType = enumType

    @t.override
    def serialize(self, value: COMMON) -> tuple[bool, t.Optional[RAW]]:
        if isinstance(value, self.COMMON):
            return True, value.name
        return False, None

    @t.override
    def deserialize(self, value: RAW) -> tuple[bool, t.Optional[COMMON]]:
        try:
            return True, self._enumType[value]
        except KeyError:
            return False, None


class BaseListField(Field):
    COMMON = list

    @t.overload
    def __init__(self, name: str, memberField: t.Type[Field] = StringField): ...
    @t.overload
    def __init__(
        self, name: str, memberField: t.Type[Field] = StringField, *, default: COMMON
    ): ...

    def __init__(self, name: str, memberField: t.Type[Field] = StringField, **kwargs):
        super().__init__(name, **kwargs)
        self._memberField = memberField("")
