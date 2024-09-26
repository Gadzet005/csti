import os

from csti.etc.language import GeneralLanguage
from csti.program_view import *
from tests.testcase import IsolatedDirCase


class TestProgram(IsolatedDirCase):
    DATA_DIR = "program_view/programs"
    TEST_DIR = "program_view/test"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.copyAll()

    def setUp(self):
        self.divide = ProgramView(self.getTestDir("divide.cpp"), GeneralLanguage.cpp)
        self.add = ProgramView(self.getTestDir("add.c"), GeneralLanguage.c)
        self.compileError = ProgramView(
            self.getTestDir("compile_error.c"), GeneralLanguage.c
        )
        self.someCode = ProgramView(
            self.getTestDir("some_code.cpp"), GeneralLanguage.cpp
        )
        self.someCodeExpected = ProgramView(
            self.getTestDir("some_code_expected.cpp"), GeneralLanguage.cpp
        )
        self.cicle = ProgramView(self.getTestDir("cicle.c"), GeneralLanguage.c)

    def testCompile(self):
        """Тестирование компиляции."""

        program = ProgramView("don't exists", GeneralLanguage.c)
        with self.assertRaises(CompileError):
            program.compile()

        with self.assertRaises(CompileError):
            self.compileError.compile()

        self.add.compile()
        self.add.compile()

    def testCAddProgram(self):
        """Компиляция и запуск программы, складывающей два числа."""

        self.add.clear()
        with self.assertRaises(RunError):
            self.add.run(timeLimit=0.1)

        with prepareForRun(self.add):
            output = self.add.run("1 2")
            self.assertEqual(output, "3\n")
            output = self.add.run("-4 -8")
            self.assertEqual(output, "-12\n")

        self.assertFalse(os.path.exists(self.add._outputFile))

        with self.assertRaises(RunError):
            self.add.run(timeLimit=0.1)

    def testCppDivideProgram(self):
        """Компиляция и запуск программы, делящей два числа."""

        self.divide.clear()
        with self.assertRaises(RunError):
            self.divide.run(timeLimit=0.1)

        with prepareForRun(self.divide):
            output = self.divide.run("10 5")
            self.assertEqual(output, "2\n")
            output = self.divide.run("18 -3")
            self.assertEqual(output, "-6\n")

            with self.assertRaises(RunError):
                self.divide.run("10 0")

        self.assertFalse(os.path.exists(self.divide._outputFile))

        with self.assertRaises(RunError):
            self.divide.run()
        self.divide.clear()

    def testFormat(self):
        """Тестирование форматирования программы."""

        program = ProgramView(self.someCode.filePath, GeneralLanguage.cpp)
        with self.assertRaises(FormatError):
            program.format("don't exists")

        formattedPath = ""
        with format(program, "msu-style") as formatted:
            formattedPath = formatted.filePath
            self.assertTrue(os.path.exists(formattedPath))

            originalOutput = run(program)
            formattedOutput = run(formatted)
            self.assertEqual(originalOutput, formattedOutput)

            self.assertEqual(self.someCodeExpected.code, formatted.code)

        self.assertFalse(os.path.exists(formattedPath))
        self.assertTrue(os.path.exists(program.filePath))

        formattedPath = os.path.join(os.path.dirname(program.filePath), "formatted")
        with format(program, "msu-style", formattedPath):
            self.assertTrue(os.path.exists(formattedPath))
        self.assertFalse(os.path.exists(formattedPath))

    def testProgramTest(self):
        """Тестирование запуска тестов для программы."""

        testCases = [
            ("10 5", "2"),
            ("9 3", "3"),
            ("10 1", "2"),
            ("10 0", "0"),
        ]

        with prepareForRun(self.divide):
            results = self.divide.test(testCases, timeLimit=1)

            self.assertEqual(results.total, 4)
            self.assertEqual(results.passed, 2)
            self.assertEqual(results[0].status, TestStatus.ok)
            self.assertEqual(results[1].status, TestStatus.ok)
            self.assertEqual(results[2].status, TestStatus.wrongAnswer)
            self.assertEqual(results[3].status, TestStatus.runtimeError)

    def testTimeout(self):
        """Тестирование превышения времени ожидания."""

        with prepareForRun(self.cicle):
            with self.assertRaises(TimeoutError):
                self.cicle.run(timeLimit=0.1)

    def testClear(self):
        """Тестирование очистки временных файлов."""

        path = self.useData("add.c", "add/add.c")
        add = ProgramView(path, GeneralLanguage.c)
        add.compile()
        add.run("1 2")
        add.clear()

        files = os.listdir(os.path.dirname(add.filePath))
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0], os.path.basename(add.filePath))

    def testNameConflict(self):
        """Тестирование конфликта имен временных файлов."""
        program1 = self.add

        path = os.path.join(os.path.dirname(self.add.filePath), "add.cpp")
        program2 = self.divide.format("msu-style", path)

        program1.compile()
        self.assertEqual(program1.run("4 2"), "6\n")
        program2.compile()
        self.assertEqual(program2.run("4 2"), "2\n")
