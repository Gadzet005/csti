import os
import unittest

from csti.etc.language import GeneralLanguage
from csti.program_view import *


class TestProgram(unittest.TestCase):
    PROGRAMS_DIR = "tests/program_view/programs"

    def setUp(self):
        self.divide = ProgramView(
            os.path.join(self.PROGRAMS_DIR, "divide.cpp"), GeneralLanguage.cpp
        )
        self.add = ProgramView(
            os.path.join(self.PROGRAMS_DIR, "add.c"), GeneralLanguage.c
        )
        self.compileError = ProgramView(
            os.path.join(self.PROGRAMS_DIR, "compile_error.c"), GeneralLanguage.c
        )
        self.some_code = ProgramView(
            os.path.join(self.PROGRAMS_DIR, "some_code.cpp"), GeneralLanguage.cpp
        )
        self.some_code_expected = ProgramView(
            os.path.join(self.PROGRAMS_DIR, "some_code_expected.cpp"),
            GeneralLanguage.cpp,
        )
        self.cicle = ProgramView(
            os.path.join(self.PROGRAMS_DIR, "cicle.c"), GeneralLanguage.c
        )

    def testCompile(self):
        """Тестирование компиляции."""

        program = ProgramView("don't exists", GeneralLanguage.c)
        with self.assertRaises(CompileError):
            program.compile()

        program = ProgramView(self.add.filePath, GeneralLanguage.nasm)
        with self.assertRaises(CompileError):
            program.compile()

        with self.assertRaises(CompileError):
            self.compileError.compile()

        with prepareForRun(self.add):
            pass

    def testCAddProgram(self):
        """Компиляция и запуск программы, складывающей два числа."""

        with self.assertRaises(RunError):
            self.add.run()

        with prepareForRun(self.add):
            output = self.add.run("1 2")
            self.assertEqual(output, "3\n")
            output = self.add.run("-4 -8")
            self.assertEqual(output, "-12\n")

        with self.assertRaises(RunError):
            self.add.run()
        self.add.clear()

    def testCppDivideProgram(self):
        """Компиляция и запуск программы, делящей два числа."""

        with self.assertRaises(RunError):
            self.divide.run()

        with prepareForRun(self.divide):
            output = self.divide.run("10 5")
            self.assertEqual(output, "2\n")
            output = self.divide.run("18 -3")
            self.assertEqual(output, "-6\n")

            with self.assertRaises(RunError):
                self.divide.run("10 0")

        with self.assertRaises(RunError):
            self.divide.run()
        self.divide.clear()

    def testFormat(self):
        """Тестирование форматирования программы."""

        program = ProgramView(self.some_code.filePath, GeneralLanguage.nasm)
        with self.assertRaises(FormatError):
            program.format("msu-style")

        program = ProgramView(program.filePath, GeneralLanguage.cpp)
        with self.assertRaises(FormatError):
            program.format("don't exists")

        with format(program, "msu-style") as formatted:
            originalOutput = run(program)
            formattedOutput = run(formatted)
            self.assertEqual(originalOutput, formattedOutput)

            self.assertEqual(self.some_code_expected.code, formatted.code)

    def testProgramTest(self):
        """Тестирование запуска тестов для программы"""

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
        """Тестирование превышения времени ожидания"""

        with prepareForRun(self.cicle):
            with self.assertRaises(TimeoutError):
                self.cicle.run(timeLimit=0.1)
