import abc
import typing as t
from enum import Enum

from csti.data_storage.template_member import TemplateMember


class Field(abc.ABC, TemplateMember):
    """Базовый класс поля в хранилище."""

    """Тип для хранения."""
    RAW = t.Any
    """Тип для использования."""
    COMMON = t.Any

    def __init__(self, name: str, defaultValue: t.Optional[COMMON]=None):
        super().__init__(name)
        self._defaultValue = defaultValue

    @property
    def defaultValue(self) -> t.Optional[COMMON]:
        return self._defaultValue

    @abc.abstractmethod
    def serialize(self, value: COMMON) -> RAW:
        """Объект для использования -> объект для хранения."""
        pass

    @abc.abstractmethod
    def deserialize(self, value: RAW) -> COMMON:
        """Объект для хранения -> объект для использования."""
        pass


class TypeField(Field):
    RAW = type
    COMMON = type

    @t.override
    def serialize(self, value: COMMON) -> RAW:
        return self.RAW(value)

    @t.override
    def deserialize(self, value: RAW) -> COMMON:
        return self.COMMON(value)


class StringField(TypeField):
    RAW = str
    COMMON = str


class EnumField(Field):
    RAW = str
    COMMON = Enum

    def __init__(
        self, 
        name: str, 
        enumType: t.Type[Enum], 
        defaultValue: t.Optional[COMMON] = None
    ):
        super().__init__(name, defaultValue)
        self._enumType = enumType

    @t.override
    def serialize(self, value: COMMON) -> RAW:
        return value.name # type: ignore

    @t.override
    def deserialize(self, value: RAW) -> COMMON:
        return self._enumType[value] # type: ignore


class BaseListField(Field):
    COMMON = list
    DEFAULT_MEMBER_FIELD = StringField

    def __init__(
        self,
        name: str,
        memberField: t.Type[Field] = DEFAULT_MEMBER_FIELD,
        separator: str = ", ",
        defaultValue: t.Optional[COMMON] = None,
    ):
        super().__init__(name, defaultValue)
        self._memberField = memberField(name="")
        self._separator = separator
