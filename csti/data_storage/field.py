import abc
from typing import Any, Type, override

from csti.data_storage.template import TemplateMember


class Field(abc.ABC, TemplateMember):
    def __init__(self, name: str, defaultValue=None):
        super().__init__(name)
        self._defaultValue = defaultValue

    @property
    def defaultValue(self) -> Any:
        return self._defaultValue

    @abc.abstractmethod
    def serialize(self, value) -> Any:
        """ Объект для использования -> объект для хранения. """
        pass

    @abc.abstractmethod
    def deserialize(self, value) -> Any:
        """ Объект для хранения -> объект для использования. """
        pass


class TypeField(Field):
    def __init__(
            self,
            name: str,
            type: Type,
            rawType: Type=str,
            defaultValue=None
        ):
        super().__init__(name, defaultValue)
        self._type = type
        self._rawType = rawType

    @override
    def serialize(self, value):
        return self._rawType(value)

    @override
    def deserialize(self, value):
        return self._type(value)


class StringField(TypeField):
    def __init__(self, name: str, defaultValue=None):
        super().__init__(name, str, str, defaultValue)


class IntField(TypeField):
    def __init__(self, name: str, defaultValue=None):
        super().__init__(name, int, str, defaultValue)


class BoolField(TypeField):
    def __init__(self, name: str, defaultValue=None):
        super().__init__(name, bool, str, defaultValue)


class ListField(Field):
    SEPARATOR = ", "

    def __init__(
            self, 
            name: str, 
            memberField: Type[Field]=StringField,
            defaultValue=None
        ):
        super().__init__(name, defaultValue)
        self._memberField = memberField(name="")

    @override
    def serialize(self, value: list[Any]):
        return self.SEPARATOR.join([
            self._memberField.serialize(item) for item in value
        ])
    
    @override
    def deserialize(self, value):
        return [
            self._memberField.deserialize(item) for item in value.split(self.SEPARATOR)
        ]
