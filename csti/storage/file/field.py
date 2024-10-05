import typing as t

from csti.storage.field import *


class IntField(Field):
    def serialize(self, value: Common) -> RawResult:
        if isinstance(value, int):
            return True, str(value)
        return False, None

    def deserialize(self, value: Raw) -> CommonResult:
        if isinstance(value, str):
            try:
                return True, int(value)
            except ValueError:
                return False, None
        return False, None


class BoolField(Field):
    @t.override
    def serialize(self, value: Common) -> RawResult:
        if isinstance(value, bool):
            return True, "1" if value else "0"
        return False, None

    @t.override
    def deserialize(self, value: Raw) -> CommonResult:
        if value == "0":
            return True, False
        if value == "1":
            return True, True
        return False, None


class ListField(BaseListField):
    @t.overload
    def __init__(
        self, name: str = "", item: Field = StringField(), separator: str = ", "
    ): ...
    @t.overload
    def __init__(
        self,
        name: str = "",
        item: Field = StringField(),
        separator: str = ", ",
        *,
        default: list
    ): ...

    def __init__(
        self,
        name: str = "",
        item: Field = StringField(),
        separator: str = ", ",
        **kwargs
    ):
        super().__init__(name, item, **kwargs)
        self._separator = separator

    @t.override
    def serialize(self, value: Common) -> RawResult:
        if not isinstance(value, list):
            return False, None

        result = []
        for item in value:
            success, serialized = self._item.serialize(item)
            if not success:
                return False, None
            result.append(serialized)

        return True, self._separator.join(result)

    @t.override
    def deserialize(self, value: Raw) -> CommonResult:
        if not isinstance(value, str):
            return False, None

        result = []
        for item in value.split(self._separator):
            success, deserialized = self._item.deserialize(item)
            if not success:
                return False, None
            result.append(deserialized)

        return True, result
