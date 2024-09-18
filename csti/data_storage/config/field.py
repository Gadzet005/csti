import typing as t

from csti.data_storage.field import *


class IntField(TypeField):
    RAW = int
    COMMON = int


class BoolField(TypeField):
    RAW = bool
    COMMON = bool


class ListField(BaseListField):
    RAW = list
    COMMON = list

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

        return True, result

    @t.override
    def deserialize(self, value: RAW) -> tuple[bool, t.Optional[COMMON]]:
        if not isinstance(value, self.RAW):
            return False, None
        result = []

        for item in value:
            success, deserialized = self._memberField.deserialize(item)
            if not success:
                return False, None
            result.append(deserialized)
        
        return True, result
