import os

from csti.data_storage.exceptions import (FieldIsEmpty, FieldNotFound,
                                          FieldValueError, LoadError)
from tests.config.configs import *
from tests.testcase import FileTestCase


class TestYAMLConfig(FileTestCase):
    DATA_DIR = "config/data"
    TEST_DIR = "config/test"

    def testIntField(self):
        config = IntConfig(self.useData("int_config.yaml"))
        config.load()

        self.assertEqual(config["number"], 150)
        self.assertEqual(config["default_number"], 1000)
        with self.assertRaises(FieldValueError):
            config["invalid_number"]

        with self.assertRaises(FieldValueError):
            config["number"] = "str"

        config["number"] = 200
        config["invalid_number"] = 0
        config.save()

        config = IntConfig(config.path)
        config.load()
        self.assertEqual(config["number"], 200)
        self.assertEqual(config["default_number"], 1000)
        self.assertEqual(config["invalid_number"], 0)
    
    def testStringField(self):
        config = StringConfig(self.useData("string_config.yaml"))
        config.load()

        self.assertEqual(config["name"], "hello world")
        self.assertEqual(config["default_name"], "Bob")
        with self.assertRaises(FieldValueError):
            config["invalid_name"]
        
        with self.assertRaises(FieldValueError):
            config["name"] = 123

        config["name"] = "new name"
        config["invalid_name"] = ""
        config.save()

        config = StringConfig(config.path)
        config.load()
        self.assertEqual(config["name"], "new name")
        self.assertEqual(config["default_name"], "Bob")
        self.assertEqual(config["invalid_name"], "")

    def testBoolField(self):
        config = BoolConfig(self.useData("bool_config.yaml"))
        config.load()

        self.assertTrue(config["is_active"])
        self.assertTrue(config["default_active"])
        with self.assertRaises(FieldValueError):
            config["invalid_flag"]

        with self.assertRaises(FieldValueError):
            config["is_active"] = "str"

        config["is_active"] = False
        config["invalid_flag"] = True
        config.save()

        config = BoolConfig(config.path)
        config.load()
        self.assertFalse(config["is_active"])
        self.assertTrue(config["default_active"])
        self.assertTrue(config["invalid_flag"])

    def testEnumField(self):
        config = EnumConfig(self.useData("enum_config.yaml"))
        config.load()

        self.assertEqual(config["color"], Color.green)
        self.assertEqual(config["default_color"], Color.red)
        with self.assertRaises(FieldValueError):
            config["invalid_color"]

        with self.assertRaises(FieldValueError):
            config["color"] = "str"

        config["color"] = Color.green
        config["invalid_color"] = Color.blue
        config.save()

        config = EnumConfig(config.path)
        config.load()
        self.assertEqual(config["color"], Color.green)
        self.assertEqual(config["default_color"], Color.red)
        self.assertEqual(config["invalid_color"], Color.blue)
    
    def testListField(self):
        config = ListConfig(self.useData("list_config.yaml"))
        config.load()

        self.assertEqual(config["numbers"], [10, 11, 12])
        self.assertEqual(config["default_numbers"], [1, 2, 3])
        self.assertEqual(config["strings"], ["hello", "world"])
        self.assertEqual(config["enums"], [Color.red, Color.green, Color.blue])
        self.assertEqual(config["default_enums"], [Color.red, Color.blue])
        self.assertEqual(config["matrix"], [[1, 1, 1], [1, 2, 3], [4, 5, 6]])
        self.assertEqual(config["default_matrix"], [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        with self.assertRaises(FieldValueError):
            config["invalid_numbers"]
        with self.assertRaises(FieldValueError):
            config["invalid_matrix"]

        with self.assertRaises(FieldValueError):
            config["numbers"] = "str"
        with self.assertRaises(FieldValueError):
            config["numbers"] = ["str"]
        with self.assertRaises(FieldValueError):
            config["matrix"] = [1, 2, 3]
        with self.assertRaises(FieldValueError):
            config["matrix"] = [[1, 2, ""], [3, 4, 5]]

        config["numbers"] = [4, 5, 6]
        config["invalid_numbers"] = []
        config["matrix"] = [[1, 2], [3, 4, 5], [6, 7, 8, 9]]
        config.save()

        config = ListConfig(config.path)
        config.load()
        self.assertEqual(config["numbers"], [4, 5, 6])
        self.assertEqual(config["invalid_numbers"], [])
        self.assertEqual(config["matrix"], [[1, 2], [3, 4, 5], [6, 7, 8, 9]])
    
    def testGroup(self):
        config = GroupConfig(self.useData("group_config.yaml"))
        config.load()

        self.assertEqual(config["num"], 1)
        self.assertEqual(config["group1", "num"], 2)
        self.assertEqual(config["group2", "group1", "num"], 3)
        self.assertEqual(config["group2", "group1", "flag"], True)
        self.assertEqual(config["group2", "group2", "num"], 4)
        self.assertEqual(config["group2", "group2", "name"], "world")

        with self.assertRaises(FieldIsEmpty):
            config["group1", "name"]
        with self.assertRaises(FieldValueError):
            config["group1", "invalid_num"]
        with self.assertRaises(FieldValueError):
            config["group2", "group1", "flag"] = None
        
        config["group2", "group2", "num"] = 10
        config["group2", "group2", "name"] = "buy"
        config.save()

        config = GroupConfig(config.path)
        config.load()
        self.assertEqual(config["group2", "group2", "num"], 10)
        self.assertEqual(config["group2", "group2", "name"], "buy")
        
    def testLoad(self):
        invalid = GroupConfig(self.useData("invalid.yaml"))
        with self.assertRaises(LoadError):
            invalid.load()

        noFound = GroupConfig(
            os.path.join(self.getTestDir(), "no_fount_config.yaml")
        )
        with self.assertRaises(LoadError):
            noFound.load()
        
        valid = GroupConfig(self.useData("group_config.yaml"))

        with self.assertRaises(FieldIsEmpty):
            valid["group1", "num"]
        valid.load()
        self.assertEqual(valid["group1", "num"], 2)
    
    def testSave(self):
        config = GroupConfig(self.useData("group_config.yaml"))
        config.load()

        config["group1", "name"] = "buy"
        config.save()

        config = GroupConfig(config.path)
        config.load()
        self.assertEqual(config["group1", "name"], "buy")

        new = GroupConfig(os.path.join(self.getTestDir(), "new.yaml"))
        new["num"] = 1
        new["group1", "num"] = 2
        new.save()
        self.assertTrue(os.path.exists(new.path))

        new = GroupConfig(new.path)
        new.load()
        self.assertEqual(new["num"], 1)
        self.assertEqual(new["group1", "num"], 2)

    def testNotFound(self):
        config = GroupConfig(self.useData("group_config.yaml"))
        config.load()

        with self.assertRaises(FieldNotFound):
            config["group1", "invalid_key"]

        with self.assertRaises(FieldNotFound):
            config["group1", "name", "invalid_key"]

        with self.assertRaises(FieldNotFound):
            config["invalid_key"]

        with self.assertRaises(FieldNotFound):
            config["group1", "group2", "invalid_key"]

        with self.assertRaises(FieldNotFound):
            config["group1", "group2", "group1", "invalid_key"]

    def testContains(self):
        config = GroupConfig(self.useData("group_config.yaml"))
        config.load()

        self.assertTrue("group1" in config)
        self.assertTrue("group1", "name" in config)
        self.assertTrue("num" in config)
        self.assertTrue(("group2", "group1") in config)
        self.assertTrue(("group2", "group2") in config)

        self.assertFalse(("group1", "invalid_key") in config)
        self.assertFalse("invalid_key" in config)
        self.assertFalse(("group1", "group2", "invalid_key") in config)
        self.assertFalse(("group1", "group2") in config)
        self.assertFalse(("no_found", "group2", "group1") in config)

    def testEmpty(self):
        config = IntConfig(self.useData("empty.yaml"))
        config.load()

        self.assertEqual(config["default_number"], 1000)

        with self.assertRaises(FieldIsEmpty):
            config["number"]
        
        config["number"] = 100
        config["default_number"] = 200
        config.save()

        config = IntConfig(config.path)
        config.load()
        self.assertEqual(config["number"], 100)
        self.assertEqual(config["default_number"], 200)

    def testCreate(self):
        config = GroupConfig(os.path.join(self.getTestDir(), "new_config.yaml"))
        config.create()
        self.assertTrue(os.path.exists(config.path))
