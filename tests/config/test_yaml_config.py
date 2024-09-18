import os
from enum import Enum

from csti.data_storage import Group, StorageTemplate
from csti.data_storage.config import YAMLConfig
from csti.data_storage.config.field import (BoolField, EnumField, IntField,
                                            ListField, StringField)
from csti.data_storage.exceptions import (FieldIsEmpty, FieldNotFound,
                                          FieldValueError, LoadError)
from tests.testcase import FileTestCase


class MyEnum(Enum):
    YES = 1
    NO = 2
    MAYBE = 3


class MyConfig(YAMLConfig):
    template = StorageTemplate(
        [
            IntField("num"),
            IntField("num-default", default=0),
            EnumField("enum", MyEnum),
            EnumField("enum-default", MyEnum, default=MyEnum.YES),
            ListField("num-list", IntField),
            ListField("num-list-default", IntField, default=[0, 8, 8, 0]),

            StringField("password"),
            Group(
                "group",
                [
                    IntField("num"),
                    ListField("invalid-num-list", IntField),
                    ListField("invalid-num-list2", IntField),
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


class TestYAMLConfig(FileTestCase):
    DATA_DIR = "config/data"
    TEST_DIR = "config/test"

    @classmethod
    def getConfig(cls):
        return MyConfig(cls.useData("config.yaml"))

    @classmethod
    def getInvalidConfig(cls):
        return MyConfig(cls.useData("invalid_config.yaml"))

    @classmethod
    def getNoFoundConfig(cls):
        path = os.path.join(cls.getTestDir(), "not_found.yaml")
        if os.path.exists(path):
            os.remove(path)
        return MyConfig(path)


    def testLoad(self):
        with self.assertRaises(LoadError):
            self.getNoFoundConfig().load()

        with self.assertRaises(LoadError):
            self.getInvalidConfig().load()

        config = self.getConfig()
        with self.assertRaises(FieldIsEmpty):
            config.get("num")

        config.load()
        self.assertEqual(config["num"], 10)

    def testSave(self):
        config = self.getNoFoundConfig()

        config["num"] = 10
        config["num-list"] = [1, 2, 3]
        config["password"] = "secret"
        config["group", "num"] = 1
        config["group", "group1", "name"] = "hello world"
        config["group", "group1", "bool-list"] = [True, False]
        config.save()

        self.assertTrue(os.path.exists(config.path))

        config = MyConfig(config.path)
        config.load()
        self.assertEqual(config["num"], 10)
        self.assertEqual(config["num-list"], [1, 2, 3])
        self.assertEqual(config["password"], "secret")
        self.assertEqual(config["group", "num"], 1)
        self.assertEqual(config["group", "group1", "name"], "hello world")
        self.assertEqual(config["group", "group1", "bool-list"], [True, False])

    def testGet(self):
        config = self.getConfig()
        config.load()

        self.assertEqual(config["num"], 10)
        self.assertEqual(config["num-list"], [1, 2, 3])
        self.assertEqual(config["group", "num"], 1)
        self.assertEqual(config["group", "group1", "name"], "hello world")
        self.assertEqual(config["enum"], MyEnum.MAYBE)
        
        # Значение по умолчанию
        self.assertFalse("enum-default" in config)
        self.assertEqual(config["enum-default"], MyEnum.YES)
        self.assertFalse("num-default" in config)
        self.assertEqual(config["num-default"], 0)
        self.assertFalse("num-list-default" in config)
        self.assertEqual(config["num-list-default"], [0, 8, 8, 0])

        with self.assertRaises(FieldNotFound):
            config.get("not_found")

        with self.assertRaises(FieldNotFound):
            config.get("group")

        with self.assertRaises(FieldNotFound):
            config.get("group", "not_found")

        with self.assertRaises(FieldIsEmpty):
            config.get("password")

        with self.assertRaises(FieldValueError):
            config["group", "invalid-num-list"]
        
        with self.assertRaises(FieldValueError):
            config["group", "invalid-num-list2"]

    def testSet(self):
        config = self.getConfig()

        config["num"] = 20
        config["group", "num"] = 2
        config["group", "group1", "name"] = "hello"
        config["group", "group1", "bool-list"] = [True, False]
        config["group", "group2", "name"] = "my name"
        config["enum"] = MyEnum.NO

        with self.assertRaises(FieldNotFound):
            config["no_found"] = False
        
        with self.assertRaises(FieldValueError):
            config["num"] = "str"

        with self.assertRaises(FieldValueError):
            config["group", "invalid-num-list"] = [1, 2, "str"]
        
        with self.assertRaises(FieldValueError):
            config["password"] = 10

        self.assertEqual(config["num"], 20)
        self.assertEqual(config["group", "num"], 2)
        self.assertEqual(config["group", "group1", "name"], "hello")
        self.assertEqual(config["group", "group1", "bool-list"], [True, False])
        self.assertEqual(config["group", "group2", "name"], "my name")
        self.assertEqual(config["enum"], MyEnum.NO)

    def testContains(self):
        config = self.getConfig()
        config.load()

        self.assertTrue("num" in config)
        self.assertTrue(("group", "num") in config)
        self.assertTrue(("group", "group1", "name") in config)

        self.assertFalse("group" in config)
        self.assertFalse(("group", "group1") in config)
        self.assertFalse("not_found" in config)
        self.assertFalse(("group", "not_found") in config)
        self.assertFalse(("group", "group1", "not_found") in config)
