import subprocess
import os
from src.tester.exceptions import (
    RuntimeError, CompileError
)
from src.consts import Language

class Tester():
    # Названия скомпилированного файла и файла с выходными данными
    compiledFileName = "program"
    outputFileName = "output.txt"

    def __init__(self, lang: Language, path: str):
        self._makefile = self.getMakefileByLang(lang)
        self._dir, self._fileName = os.path.split(path)

    @staticmethod
    def getMakefileByLang(lang: Language):
        dir = os.path.dirname(__file__)
        match lang:
            case Language.c:
                return os.path.join(dir, "make/c")
            case Language.cpp:
                return os.path.join(dir, "make/cpp")
            case Language.asm:
                return os.path.join(dir, "make/asm")
            case _:
                raise ValueError(f"Неподдерживаемый язык: {lang}")

    # Убирает лишние пробелы и строки
    @staticmethod
    def normalizeOutput(output: str) -> str:
        lines = output.split('\n')
        lines = map(
            lambda line: " ".join(filter(lambda x: x != "", line.split(' '))), 
            lines
        )
        lines = filter(lambda x: x != "", lines)

        return '\n'.join(lines)

    # Компиляция программы
    def compileProgram(self):
        result = subprocess.run(
            [
                "make", "compile", "-f", self._makefile, 
                f"DIR={self._dir}", f"FILE={self._fileName}"
            ], capture_output=True
        )

        if result.returncode != 0:
            raise CompileError(result.stderr.decode())

    # Запуск программы. Возращает вывод программы
    def runProgram(self, input: str) -> str:
        result = subprocess.run(
            [
                "make", "run", "-f", self._makefile, f"DIR={self._dir}",
            ], capture_output=True, input=input.encode()
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr.decode())
        
        output = open(os.path.join(self._dir, self.outputFileName), 'r').read()
        return output.strip()

    # Очистка временных файлов
    def clear(self):
        subprocess.run(
            ["make", "clear", "-f", self._makefile, f"DIR={self._dir}",], capture_output=True
        )

    """
    Запуск тестов. Выводит результаты тестов
    testCases: [(Вход, Ожидаемый выход), ...]
    Возвращает успешно ли пройдены все тесты.
    """
    def runTests(self, testCases: list[str, str]):
        testPassed = True

        try:
            self.compileProgram()
        except CompileError as error:
            print(f">>> Ошибка компиляции файла '{self._fileName}' \n{error.message}")
            return False
        
        testCount = len(testCases)
        print(f">>> Запуск тестов: {testCount}")
        for idx, (input, expected) in enumerate(testCases, 1):
            print(f">>> [{idx}/{testCount}]", end=" ")
            try:
                output = self.normalizeOutput(self.runProgram(input))
                expected = self.normalizeOutput(expected)

                if output != expected:
                    print(
                        f"Неправильный ответ\nВходные данные:\n{input}\n"
                        f"Выходные данные:\n{output}\nОжидаемые выходные данные:\n{expected}"
                    )
                else:
                    print("OK")
            except RuntimeError:
                print(f"Ошибка выполнения")
        
        self.clear()
        
        return testPassed
    
