import typing as t

from csti.data_storage.field import *


class IntField(Field):
    def serialize(self, value: int) -> tuple[bool, t.Optional[str]]:
        if isinstance(value, int):
            return True, str(value)
        return False, None
    
    def deserialize(self, value: str) -> tuple[bool, t.Optional[int]]:
        if isinstance(value, str):
            try:
                return True, int(value)
            except ValueError:
                return False, None
        return False, None


class BoolField(Field):
    @t.override
    def serialize(self, value: bool) -> tuple[bool, t.Optional[str]]:
        if isinstance(value, bool):
            return True, "1" if value else "0"
        return False, None

    @t.override
    def deserialize(self, value: str) -> tuple[bool, t.Optional[bool]]:
        if value == "0":
            return True, False
        if value == "1":
            return True, True
        return False, None


class ListField(BaseListField):
    @t.overload
    def __init__(
        self, 
        name: str = "", 
        item: Field = StringField(),
        separator: str = ", "
    ): ...
    @t.overload
    def __init__(
        self, 
        name: str = "", 
        item: Field = StringField(),
        separator: str = ", ",
        *, default: list
    ): ...

    def __init__(
        self,
        name: str="",
        item: Field = StringField(),
        separator: str = ", ",
        **kwargs
    ):
        super().__init__(name, item, **kwargs)
        self._separator = separator

    @t.override
    def serialize(self, value: list) -> tuple[bool, t.Optional[str]]:
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
    def deserialize(self, value: str) -> tuple[bool, t.Optional[list]]:
        if not isinstance(value, str):
            return False, None

        result = []
        for item in value.split(self._separator):
            success, deserialized = self._item.deserialize(item)
            if not success:
                return False, None
            result.append(deserialized)
        
        return True, result
