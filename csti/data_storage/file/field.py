import typing as t

from csti.data_storage.field import *

class IntField(TypeField):
    RAW = str
    COMMON = int


class BoolField(TypeField):
    RAW = str
    COMMON = bool

    @t.override
    def serialize(self, value: COMMON) -> tuple[bool, t.Optional[RAW]]: # type: ignore
        if not isinstance(value, self.COMMON):
            return False, None
        return True, self.RAW(int(value))

    @t.override
    def deserialize(self, value: RAW) -> tuple[bool, t.Optional[COMMON]]: # type: ignore
        if not isinstance(value, self.RAW):
            return False, None
        try:
            return True, self.COMMON(int(value))
        except ValueError:
            return False, None

class ListField(BaseListField):
    RAW = str
    COMMON = list
    
    @t.overload
    def __init__(
        self, 
        name: str, 
        memberField: t.Type[Field] = StringField,
        separator: str = ", "
    ): ...
    @t.overload
    def __init__(
        self, 
        name: str, 
        memberField: t.Type[Field] = StringField,
        separator: str = ", ",
        *, default
    ): ...

    def __init__(
        self,
        name: str,
        memberField: t.Type[Field] = StringField,
        separator: str = ", ",
        **kwargs
    ):
        super().__init__(name, memberField, **kwargs)
        self._separator = separator

    @t.override
    def serialize(self, value: COMMON) -> tuple[bool, t.Optional[RAW]]:
        if not isinstance(value, self.COMMON):
            return False, None
        result = []

        for item in value:
            success, serialized = self._memberField.serialize(item)
            if not success:
                return False, None
            result.append(serialized)

        return True, self._separator.join(result)

    @t.override
    def deserialize(self, value: RAW) -> tuple[bool, t.Optional[COMMON]]:
        if not isinstance(value, self.RAW):
            return False, None
        result = []

        for item in value.split(self._separator):
            success, deserialized = self._memberField.deserialize(item)
            if not success:
                return False, None
            result.append(deserialized)
        
        return True, result
