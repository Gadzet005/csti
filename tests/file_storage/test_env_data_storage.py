import os
from enum import Enum

from csti.data_storage import Group, StorageTemplate
from csti.data_storage.file import FileStorage
from csti.data_storage.file.field import (BoolField, EnumField, IntField,
                                          ListField, StringField)
from csti.data_storage.exceptions import (FieldIsEmpty, FieldNotFound,
                                          FieldValueError)
from tests.testcase import FileTestCase


class MyEnum(Enum):
    YES = 1
    NO = 2
    MAYBE = 3


class MyStorage(FileStorage):
    def __init__(self, dir):
        super().__init__()
        self.dir = dir

    template = StorageTemplate(
        [
            IntField("num"),
            IntField("num-default", default=0),
            EnumField("enum", MyEnum),
            EnumField("enum-default", MyEnum, default=MyEnum.YES),
            ListField("num-list", IntField, separator="\n"),
            ListField("num-list-default", IntField, default=[0, 8, 8, 0]),

            StringField("password"),
            Group(
                "group",
                [
                    IntField("num"),
                    ListField("invalid-num-list", IntField),
                    Group(
                        "group1",
                        [StringField("name"), ListField("bool-list", BoolField)],
                    ),
                    Group(
                        "group2",
                        [StringField("name")]
                    ),
                ],
            ),
            Group("empty", []),
        ]
    )

    def getPathByLocation(self, location: tuple[str, ...]) -> str:
        return os.path.join(self.dir, *location)
    
    def create(self):
        os.makedirs(self.dir, exist_ok=True)


class TestFileStorage(FileTestCase):
    DATA_DIR = "file_storage/data"
    TEST_DIR = "file_storage/test"

    @classmethod
    def getStorage(cls):
        return MyStorage(cls.useData("storage", isDir=True))

    def testGet(self):
        storage = self.getStorage()

        self.assertEqual(storage["num"], 10)
        self.assertEqual(storage["num-list"], [1, 2, 3])
        self.assertEqual(storage["group", "num"], 1)
        self.assertEqual(storage["group", "group1", "name"], "hello world")
        self.assertEqual(storage["enum"], MyEnum.MAYBE)
        
        # Значение по умолчанию
        self.assertFalse("enum-default" in storage)
        self.assertEqual(storage["enum-default"], MyEnum.YES)
        self.assertFalse("num-default" in storage)
        self.assertEqual(storage["num-default"], 0)
        self.assertFalse("num-list-default" in storage)
        self.assertEqual(storage["num-list-default"], [0, 8, 8, 0])

        with self.assertRaises(FieldNotFound):
            storage.get("not_found")

        with self.assertRaises(FieldNotFound):
            storage.get("group")

        with self.assertRaises(FieldNotFound):
            storage.get("group", "not_found")

        with self.assertRaises(FieldIsEmpty):
            storage.get("password")

        with self.assertRaises(FieldValueError):
            storage["group", "invalid-num-list"]

    def testSet(self):
        storage = self.getStorage()

        storage["num"] = 20
        storage["group", "num"] = 2
        storage["group", "group1", "name"] = "hello"
        storage["group", "group1", "bool-list"] = [True, False]
        storage["group", "group2", "name"] = "my name"
        storage["enum"] = MyEnum.NO

        with self.assertRaises(FieldNotFound):
            storage["no_found"] = False
        
        with self.assertRaises(FieldValueError):
            storage["num"] = "str"

        with self.assertRaises(FieldValueError):
            storage["group", "invalid-num-list"] = [1, 2, "str"]
        
        with self.assertRaises(FieldValueError):
            storage["password"] = 10

        self.assertEqual(storage["num"], 20)
        self.assertEqual(storage["group", "num"], 2)
        self.assertEqual(storage["group", "group1", "name"], "hello")
        self.assertEqual(storage["group", "group1", "bool-list"], [True, False])
        self.assertEqual(storage["group", "group2", "name"], "my name")
        self.assertEqual(storage["enum"], MyEnum.NO)

    def testContains(self):
        storage = self.getStorage()

        self.assertTrue("num" in storage)
        self.assertTrue(("group", "num") in storage)
        self.assertTrue(("group", "group1", "name") in storage)

        self.assertFalse("group" in storage)
        self.assertFalse(("group", "group1") in storage)
        self.assertFalse("not_found" in storage)
        self.assertFalse(("group", "not_found") in storage)
        self.assertFalse(("group", "group1", "not_found") in storage)
