import typing as t

from csti.data_storage.field import *


class IntField(TypeField):
    RAW = int
    COMMON = int


class BoolField(TypeField):
    RAW = bool
    COMMON = bool


class ListField(BaseListField):
    RAW = BaseListField.RAW
    COMMON = BaseListField.COMMON

    @t.override
    def serialize(self, value: COMMON) -> RAW:
        return [self._memberField.serialize(item) for item in value]

    @t.override
    def deserialize(self, value: RAW) -> COMMON:
        return [self._memberField.deserialize(item) for item in value]
