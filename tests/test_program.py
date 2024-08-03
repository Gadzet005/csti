import os
import unittest

from src.program import *
from src.consts import Language

class TestProgram(unittest.TestCase):
    def testCompile(self):
        """ Тестирование компиляции """

        program = Program(Language.c, "i don't exists")
        with self.assertRaises(CompileError):
            program.compile()

        program = Program(Language.asm, "tests/programs/add.c")
        with self.assertRaises(CompileError):
            program.compile()

        program = Program(Language.c, "tests/programs/compile_error.c")
        with self.assertRaises(CompileError):
            program.compile()

        program = Program(Language.c, "tests/programs/add.c")
        program.compile()
        program.clear()

    def testCAddProgram(self):
        """ Компиляция и запуск программы, складывающей два числа """

        add = Program(Language.c, "tests/programs/add.c")

        with self.assertRaises(RunError):
            add.run()

        add.compile()

        output = add.run("1 2")
        self.assertEqual(output, "3\n")
        output = add.run("-4 -8")
        self.assertEqual(output, "-12\n")

        with self.assertRaises(TimeoutError):
            add.run(timeout=0.1)

        add.clear()

        with self.assertRaises(RunError):
            add.run()

        add.clear()
    
    def testCppDivideProgram(self):
        """ Компиляция и запуск программы, делящей два числа """

        divide = Program(Language.cpp, "tests/programs/divide.cpp")

        with self.assertRaises(RunError):
            divide.run()

        divide.compile()

        output = divide.run("10 5")
        self.assertEqual(output, "2\n")
        output = divide.run("18 -3")
        self.assertEqual(output, "-6\n")

        with self.assertRaises(TimeoutError):
            divide.run(timeout=0.1)
        
        with self.assertRaises(RunError):
            divide.run("10 0")

        divide.clear()

        with self.assertRaises(RunError):
            divide.run()

        divide.clear()

    def testSwitchProgram(self):
        """ Тестирование смены языка и пути у программы """

        program = Program(Language.c, "tests/programs/add.c")
        program.lang = Language.asm

        with self.assertRaises(CompileError):
            program.compile()
        
        program.lang = Language.cpp
        program.filePath = "tests/programs/divide.cpp"

        program.compile()
        output = program.run("10 5")
        self.assertEqual(output, "2\n")

        program.clear()

    def testFormat(self):
        """ Тестирование форматирования программы """

        program = Program(Language.asm, "tests/programs/wtf.cpp")
        with self.assertRaises(NotSupportedLanguage):
            program.format()

        program = Program(Language.cpp, "tests/programs/wtf.cpp")
        formatted = program.format()

        program.compile()
        original_output = program.run()
        program.clear()

        formatted.compile()
        formatted_output = formatted.run()
        formatted.clear()

        self.assertEqual(original_output, formatted_output)

        with open(f"tests/programs/expected_wtf.cpp", "r") as file:
            expected_code = file.read()
        with open(f"tests/programs/{formatted.file}", "r") as file:
            formatted_code = file.read()

        self.assertEqual(expected_code, formatted_code)

        os.remove(formatted.filePath)
    
    def testProgramTest(self):
        """ Тестирование запуска тестов для программы """

        testCases = [
            ("10 5", "2"),
            ("9 3", "3"),
            ("10 1", "2"),
            ("10 0", "0"),
            ("", ""),
        ]

        divide = Program(Language.cpp, "tests/programs/divide.cpp")
        divide.compile()
        results = divide.test(testCases, timeout=1)

        self.assertEqual(results.testsTotal, 5)
        self.assertEqual(results.testsPassed, 2)
        self.assertEqual(results[0].status, TestStatus.ok)
        self.assertEqual(results[1].status, TestStatus.ok)
        self.assertEqual(results[2].status, TestStatus.wrongAnswer)
        self.assertEqual(results[3].status, TestStatus.runtimeError)
        self.assertEqual(results[4].status, TestStatus.timeLimit)

        divide.clear()
