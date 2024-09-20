import os

from csti.data_storage.exceptions import (FieldIsEmpty, FieldNotFound,
                                          FieldValueError)
from tests.file_storage.storages import *
from tests.testcase import IsolatedDirCase


class TestFileStorage(IsolatedDirCase):
    DATA_DIR = "file_storage/data"
    TEST_DIR = "file_storage/test"

    def testIntField(self):
        storage = IntStorage(self.useData("int_storage", isDir=True))

        self.assertEqual(storage["number"], 150)
        self.assertEqual(storage["default_number"], 1000)
        with self.assertRaises(FieldValueError):
            storage["invalid_number"]

        with self.assertRaises(FieldValueError):
            storage["number"] = "str"

        storage["number"] = 200
        storage["invalid_number"] = 0

        self.assertEqual(storage["number"], 200)
        self.assertEqual(storage["default_number"], 1000)
        self.assertEqual(storage["invalid_number"], 0)

    def testStringField(self):
        storage = StringStorage(self.useData("string_storage", isDir=True))

        self.assertEqual(storage["name"], "hello world")
        self.assertEqual(storage["default_name"], "Bob")

        with self.assertRaises(FieldValueError):
            storage["name"] = 123

        storage["name"] = "new name"
        storage["default_name"] = ""

        self.assertEqual(storage["name"], "new name")
        self.assertEqual(storage["default_name"], "")

    def testBoolField(self):
        storage = BoolStorage(self.useData("bool_storage", isDir=True))

        self.assertTrue(storage["is_active"])
        self.assertTrue(storage["default_active"])

        with self.assertRaises(FieldValueError):
            storage["invalid_flag"]
        with self.assertRaises(FieldValueError):
            storage["is_active"] = "str"

        storage["is_active"] = False
        storage["default_active"] = True

        self.assertFalse(storage["is_active"])
        self.assertTrue(storage["default_active"])

    def testEnumField(self):
        storage = EnumStorage(self.useData("enum_storage", isDir=True))

        self.assertEqual(storage["color"], Color.green)
        self.assertEqual(storage["default_color"], Color.red)

        with self.assertRaises(FieldValueError):
            storage["invalid_color"]
        with self.assertRaises(FieldValueError):
            storage["color"] = "str"

        storage["color"] = Color.green
        storage["invalid_color"] = Color.blue

        self.assertEqual(storage["color"], Color.green)
        self.assertEqual(storage["invalid_color"], Color.blue)

    def testListField(self):
        storage = ListStorage(self.useData("list_storage", isDir=True))

        self.assertEqual(storage["numbers"], [10, 12, 13])
        self.assertEqual(storage["default_numbers"], [1, 2, 3])
        self.assertEqual(storage["strings"], ["hello", "world"])
        self.assertEqual(storage["enums"], [Color.red, Color.blue])
        self.assertEqual(storage["default_enums"], [Color.red, Color.blue])
        self.assertEqual(storage["matrix"], [[1, 1, 1], [1, 2, 3], [4, 5, 6]])
        self.assertEqual(storage["default_matrix"], [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        with self.assertRaises(FieldValueError):
            storage["invalid_numbers"]
        with self.assertRaises(FieldValueError):
            storage["invalid_matrix"]

        with self.assertRaises(FieldValueError):
            storage["numbers"] = "str"
        with self.assertRaises(FieldValueError):
            storage["numbers"] = ["str"]
        with self.assertRaises(FieldValueError):
            storage["strings"] = [1, 2, 3]
        with self.assertRaises(FieldValueError):
            storage["enums"] = [1, 2, 3]
        with self.assertRaises(FieldValueError):
            storage["matrix"] = [1, 2, 3]

        storage["numbers"] = [4, 5, 6]
        storage["strings"] = ["new", "string"]
        storage["enums"] = [Color.green, Color.blue]
        storage["matrix"] = [[10, 10, 10], [10, 20, 30]]

        self.assertEqual(storage["numbers"], [4, 5, 6])
        self.assertEqual(storage["strings"], ["new", "string"])
        self.assertEqual(storage["enums"], [Color.green, Color.blue])
        self.assertEqual(storage["matrix"], [[10, 10, 10], [10, 20, 30]])

    def testGroup(self):
        storage = GroupStorage(self.useData("group_storage", isDir=True))

        self.assertEqual(storage["num"], 1)
        self.assertEqual(storage["group1", "num"], 2)
        self.assertEqual(storage["group2", "group1", "num"], 3)
        self.assertEqual(storage["group2", "group1", "flag"], True)
        self.assertEqual(storage["group2", "group2", "num"], 4)
        self.assertEqual(storage["group2", "group2", "name"], "world")

        with self.assertRaises(FieldIsEmpty):
            storage["group1", "name"]
        with self.assertRaises(FieldValueError):
            storage["group1", "invalid_num"]
        with self.assertRaises(FieldValueError):
            storage["group1", "num"] = "str"

        storage["group1", "name"] = "new name"
        storage["group1", "invalid_num"] = 0

        self.assertEqual(storage["group1", "name"], "new name")
        self.assertEqual(storage["group1", "invalid_num"], 0)

    def testNotFound(self):
        storage = GroupStorage(self.useData("group_storage", isDir=True))

        with self.assertRaises(FieldNotFound):
            storage["non_existent_field"]
        with self.assertRaises(FieldNotFound):
            storage["group1", "non_existent_subfield"]

        noFound = GroupStorage(self.getTestDir("no_found"))
        with self.assertRaises(FieldIsEmpty):
            noFound["num"]
        with self.assertRaises(FieldIsEmpty):
            noFound["group1", "num"]

    def testContains(self):
        storage = GroupStorage(self.useData("group_storage", isDir=True))

        self.assertTrue("group1" in storage)
        self.assertTrue("num" in storage)
        self.assertTrue(("group2", "group2") in storage)
        self.assertTrue(("group2", "group1", "num") in storage)
        self.assertTrue(("group2", "group1", "flag") in storage)
        self.assertTrue(("group2", "group2", "num") in storage)
        self.assertTrue(("group2", "group2", "name") in storage)

        self.assertFalse(("group1", "name") in storage)
        self.assertFalse(("group1", "invalid_key") in storage)
        self.assertFalse("invalid_key" in storage)
        self.assertFalse(("group1", "group2") in storage)

    def testCreate(self):
        storage = GroupStorage(self.getTestDir("new"))
        storage.create()
        self.assertTrue(os.path.exists(storage.dir))
