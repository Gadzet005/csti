import typing as t

from csti.storage.field import *


class IntField(Field):
    def serialize(self, value: Common) -> RawResult:
        if isinstance(value, int):
            return True, value
        return False, None

    def deserialize(self, value: Raw) -> CommonResult:
        if isinstance(value, int):
            return True, value
        return False, None


class BoolField(Field):
    def serialize(self, value: Common) -> RawResult:
        if isinstance(value, bool):
            return True, value
        return False, None

    def deserialize(self, value: Raw) -> CommonResult:
        if isinstance(value, bool):
            return True, value
        return False, None


class ListField(BaseListField):
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

        return True, result

    @t.override
    def deserialize(self, value: Raw) -> CommonResult:
        if not isinstance(value, list):
            return False, None

        result = []
        for item in value:
            success, deserialized = self._item.deserialize(item)
            if not success:
                return False, None
            result.append(deserialized)

        return True, result
