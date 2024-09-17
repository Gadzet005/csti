import os
import unittest

from csti.config import YAMLConfig
from csti.config.field import IntField, ListField, BoolField, StringField
from csti.data_storage import StorageTemplate, Group
from csti.data_storage.exceptions import FieldIsEmpty, FieldNotFound, LoadError, SaveError


class MyConfig(YAMLConfig):
    template = StorageTemplate([
        IntField("num"),
        ListField("num-list", IntField),
        StringField("password"),
        Group("group", [
            IntField("num"),
            ListField("num-list", IntField),
            Group("group", [
                StringField("name"),
                ListField("bool-list", BoolField)
            ])
        ]),
        Group("empty", [])
    ])


class TestYAMLConfig(unittest.TestCase):
    DATA_DIR = "tests/data_storage/data"

    @classmethod
    def getConfig(cls):
        return MyConfig(os.path.join(cls.DATA_DIR, "config.yaml"))

    @classmethod 
    def getNoFoundConfig(cls):
        return MyConfig(os.path.join(cls.DATA_DIR, "no_found.yaml"))

    @classmethod
    def getInvalidConfig(cls):
        return MyConfig(os.path.join(cls.DATA_DIR, "invalid.yaml"))


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
        self.assertFalse(os.path.exists(config.path))

        with self.assertRaises(FieldIsEmpty):
            config.get("num")

        config["num"] = 10
        config["num-list"] = [1, 2, 3]
        config["password"] = "secret"
        config["group", "num"] = 1
        config["group", "group", "name"] = "hello world"
        config["group", "group", "bool-list"] = [True, False]
        config.save()

        self.assertTrue(os.path.exists(config.path))

        config.load()
        self.assertEqual(config["num"], 10)
        self.assertEqual(config["num-list"], [1, 2, 3])
        self.assertEqual(config["password"], "secret")
        self.assertEqual(config["group", "num"], 1)
        self.assertEqual(config["group", "group", "name"], "hello world")
        self.assertEqual(config["group", "group", "bool-list"], [True, False])

        os.remove(config.path)

    def testGet(self):
        config = self.getConfig()
        config.load()

        self.assertEqual(config["num"], 10)
        self.assertEqual(config["num-list"], [1, 2, 3])
        self.assertEqual(config["group", "num"], 1)
        self.assertEqual(config["group", "group", "name"], "hello world")

        with self.assertRaises(FieldNotFound):
            config.get("not_found")
        
        with self.assertRaises(FieldNotFound):
            config.get("group")
        
        with self.assertRaises(FieldNotFound):
            config.get("group", "not_found")
        
        with self.assertRaises(FieldIsEmpty):
            config.get("password")

    def testSet(self):
        config = self.getNoFoundConfig()

        config["num"] = 20
        config["group", "num"] = 2
        config["group", "group", "name"] = "hello"
        config["group", "group", "bool-list"] = [True, False]

        self.assertEqual(config["num"], 20)
        self.assertEqual(config["group", "num"], 2)
        self.assertEqual(config["group", "group", "name"], "hello")
        self.assertEqual(config["group", "group", "bool-list"], [True, False])

    def testContains(self):
        config = self.getConfig()
        config.load()

        self.assertTrue("num" in config)
        self.assertTrue("group" in config)
        self.assertTrue(("group", "num") in config)
        self.assertTrue(("group", "group") in config)
        self.assertTrue(("group", "group", "name") in config)

        self.assertFalse("not_found" in config)
        self.assertFalse(("group", "not_found") in config)
        self.assertFalse(("group", "group", "not_found") in config)
