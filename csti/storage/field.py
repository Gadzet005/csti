import abc
import typing as t
from enum import Enum

from csti.storage.template_element import TemplateElement

# Тип для хранения.
Raw: t.TypeAlias = t.Any
RawResult: t.TypeAlias = tuple[bool, t.Optional[Raw]]

# Тип для использования.
Common: t.TypeAlias = t.Any
CommonResult: t.TypeAlias = tuple[bool, t.Optional[Common]]


class Field(abc.ABC, TemplateElement):
    """Базовый класс поля в хранилище."""

    @t.overload
    def __init__(self, name: str = ""): ...
    @t.overload
    def __init__(self, name: str = "", *, default: Common): ...

    def __init__(self, name: str = "", **kwargs):
        super().__init__(name)

        self._hasDefault = "default" in kwargs
        self._default = kwargs.pop("default", None)

    @property
    def default(self) -> tuple[bool, Common]:
        """
        Кортеж из двух элементов: имеется ли значение
        по умолчанию и значение по умолчанию или `None`
        """
        return self._hasDefault, self._default

    @abc.abstractmethod
    def serialize(self, value: Common) -> RawResult:
        """
        Объект для использования -> объект для хранения.
        Возвращает кортеж из двух элементов:
        успех/неудача и преобразованный объект/`None`.
        """
        pass

    @abc.abstractmethod
    def deserialize(self, value: Raw) -> CommonResult:
        """
        Объект для хранения -> объект для использования.
        Возвращает кортеж из двух элементов:
        успех/неудача и преобразованный объект/`None`.
        """
        pass


class StringField(Field):
    @t.override
    def serialize(self, value: Common) -> RawResult:
        try:
            return True, str(value)
        except ValueError:
            return False, None

    @t.override
    def deserialize(self, value: Raw) -> CommonResult:
        try:
            return True, str(value)
        except ValueError:
            return False, None


class EnumField(Field):
    @t.overload
    def __init__(self, name: str = "", *, enumType: t.Type[Enum]): ...
    @t.overload
    def __init__(self, name: str = "", *, enumType: t.Type[Enum], default: Enum): ...

    def __init__(self, name: str = "", *, enumType: t.Type[Enum], **kwargs):
        super().__init__(name, **kwargs)
        self._enumType = enumType

    @t.override
    def serialize(self, value: Common) -> RawResult:
        if isinstance(value, Enum):
            return True, value.name
        return False, None

    @t.override
    def deserialize(self, value: Raw) -> CommonResult:
        try:
            return True, self._enumType[value]
        except KeyError:
            return False, None


class BaseListField(Field):
    @t.overload
    def __init__(self, name: str = "", item: Field = StringField()): ...
    @t.overload
    def __init__(
        self, name: str = "", item: Field = StringField(), *, default: list
    ): ...

    def __init__(self, name: str = "", item: Field = StringField(), **kwargs):
        super().__init__(name, **kwargs)
        self._item = item
