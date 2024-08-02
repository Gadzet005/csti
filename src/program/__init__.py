from __future__ import annotations

import os
import subprocess

from src.consts import Language
from src.program.exceptions import (
    CompileError, FormatError, NotSupportedLanguage, RunError,
    TimeoutError
)
from src.program.make_info import MakeInfo
from src.program.utils import normalizeText


class Program:
    """ 
    Выполняет запуск, компиляцию, форматирование и 
    тестирование программы на заданном языке 
    """

    def __init__(self, lang: Language, filePath: str):
        self.lang = lang
        self.filePath = filePath


    def compile(self):
        """ Компилирует программу """

        if not self._makeInfo.canBeCompiled:
            raise NotSupportedLanguage(self.lang)

        result = subprocess.run([
            "make", MakeInfo.Target.compile.value, "-f", self._makeInfo.makefile, 
            f"DIR={self.dir}", 
            f"FILE={self.file}", 
            f"COMPILED_FILE={self.compiledFile}"
        ], capture_output=True
        )

        if result.returncode != 0:
            raise CompileError(result.stderr.decode())
    
    def run(self, input: str|None = None, timeout: str|None = None) -> str:
        """ 
        Запускает программу и возвращает её вывод. 
        Если язык компилируемый, то требуется вызов метода compile
        """

        inputBuffer = input.encode() if input else None

        try:
            result = subprocess.run([
                    "make", MakeInfo.Target.run.value, "-f", self._makeInfo.makefile,
                    f"DIR={self.dir}",
                    f"COMPILED_FILE={self.compiledFile}", 
                    f"OUTPUT_FILE={self.outputFile}",
                ], capture_output=True, input=inputBuffer, timeout=timeout
            )
        except subprocess.TimeoutExpired:
            raise TimeoutError

        if result.returncode != 0:
            raise RunError(result.stderr.decode())
        
        output = open(os.path.join(self.dir, self.outputFile), 'r').read()
        return output

    def format(self) -> Program:
        """ 
        Выполняет форматирование программы, возвращает экземпляр 
        Program для отформатированного файла 
        """

        if not self._makeInfo.canBeFormatted:
            raise NotSupportedLanguage(self.lang)

        result = subprocess.run([
                "make", MakeInfo.Target.format.name, "-f", self._makeInfo.makefile,
                f"FORMAT_CONFIG={self._makeInfo.formatConfig}",
                f"DIR={self.dir}", 
                f"FILE={self.file}", 
                f"FORMATTED_FILE={self.formattedFile}"
            ], capture_output=True
        )

        if result.returncode != 0:
            raise FormatError(result.stderr.decode())

        return Program(self.lang, os.path.join(self.dir, self.formattedFile))

    def clear(self):
        """ Очистка временных файлов """

        subprocess.run([
            "make", MakeInfo.Target.clear.name, "-f", self._makeInfo.makefile, 
            f"DIR={self.dir}",
            f"COMPILED_FILE={self.compiledFile}", 
            f"OUTPUT_FILE={self.outputFile}"
        ], capture_output=True
        )

    def test(self, testCases: list[tuple[str, str]], timeout: str|None = None) -> bool:
        """
        Запуск тестов. Выводит результаты тестов
        testCases: [(Вход, Ожидаемый выход), ...]
        Возвращает успешно ли пройдены все тесты.
        Если язык компилируемый, то требуется вызов метода compile
        """

        if (len(testCases) == 0): 
            return True

        allTestPassed = True
        testCount = len(testCases)

        print(f">>> Запуск тестов: {testCount}")
        for idx, (input, expected) in enumerate(testCases, 1):
            print(f">>> [{idx}/{testCount}]", end=" ")
            try:
                output = normalizeText(self.run(input, timeout))
                expected = normalizeText(expected)

                if output != expected:
                    print(
                        f"Неправильный ответ\nВходные данные:\n{input}\n"
                        f"Выходные данные:\n{output}\nОжидаемые выходные данные:\n{expected}"
                    )
                    allTestPassed = False
                else:
                    print("OK")
            except RunError as error:
                print(f"Ошибка выполнения\n{error}")
                allTestPassed = False
            except TimeoutError:
                print(f"Превышено максимальное время выполнения")
                allTestPassed = False

        return allTestPassed


    @property
    def filePath(self):
        """ Полный путь к файлу """
        return self._filePath
    
    @filePath.setter
    def filePath(self, filePath: str):
        self._filePath = filePath
        self._dir, self._file = os.path.split(filePath)
        self._fileName, self._fileExt = os.path.splitext(self._file)

    @property
    def dir(self):
        """ Дирректория файла """
        return self._dir
    
    @property
    def file(self):
        """ Название файла (с расширением) """
        return self._file
    
    @property
    def compiledFile(self):
        """ Файл после компиляции """
        return self.fileName + "-compiled"

    @property
    def outputFile(self):
        """ Выходные данные файла """
        return self.fileName + "-output.txt"

    @property
    def formattedFile(self):
        """ Файл после форматирования """
        return self.fileName + "-formatted" + self.fileExt

    @property
    def fileName(self):
        """ Название файла (без расширения) """
        return self._fileName
    
    @property
    def fileExt(self):
        """ Расширение файла (с точкой) """
        return self._fileExt

    @property
    def lang(self):
        """ Язык программирования """
        return self._lang
    
    @lang.setter
    def lang(self, lang: Language):
        self._lang = lang
        self._makeInfo = MakeInfo(lang)
