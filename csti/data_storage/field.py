import abc
import typing as t
from enum import Enum

from csti.data_storage.template_member import TemplateMember


class Field(abc.ABC, TemplateMember):
    def __init__(self, name: str, defaultValue=None):
        super().__init__(name)
        self._defaultValue = defaultValue

    @property
    def defaultValue(self) -> t.Any:
        return self._defaultValue

    @abc.abstractmethod
    def serialize(self, value) -> t.Any:
        """Объект для использования -> объект для хранения."""
        pass

    @abc.abstractmethod
    def deserialize(self, value) -> t.Any:
        """Объект для хранения -> объект для использования."""
        pass


class TypeField(Field):
    def __init__(
        self, name: str, type: t.Type, rawType: t.Type = str, defaultValue=None
    ):
        super().__init__(name, defaultValue)
        self._type = type
        self._rawType = rawType

    @t.override
    def serialize(self, value):
        return self._rawType(value)

    @t.override
    def deserialize(self, value):
        return self._type(value)


class StringField(TypeField):
    def __init__(self, name: str, defaultValue=None):
        super().__init__(name, str, str, defaultValue)


class IntField(TypeField):
    def __init__(self, name: str, defaultValue=None):
        super().__init__(name, int, int, defaultValue)


class BoolField(TypeField):
    def __init__(self, name: str, defaultValue=None):
        super().__init__(name, bool, bool, defaultValue)


class ListField(Field):
    def __init__(
        self,
        name: str,
        memberField: t.Type[Field] = StringField,
        separator: str = ", ",
        defaultValue=None,
    ):
        super().__init__(name, defaultValue)
        self._memberField = memberField(name="")
        self._separator = separator

    @t.override
    def serialize(self, value: list):
        return self._separator.join(
            [self._memberField.serialize(item) for item in value]
        )

    @t.override
    def deserialize(self, value):
        return [
            self._memberField.deserialize(item) for item in value.split(self._separator)
        ]


class EnumField(Field):
    def __init__(self, name: str, enumType: t.Type[Enum], defaultValue=None):
        super().__init__(name, defaultValue)
        self._enumType = enumType

    @t.override
    def serialize(self, value):
        return value.name

    @t.override
    def deserialize(self, value):
        return self._enumType[value]
