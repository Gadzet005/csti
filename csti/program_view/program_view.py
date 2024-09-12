import os
import subprocess
from typing import Self

from csti.etc.language import Language
from csti.program_view.exceptions import (CompileError, FormatError, RunError,
                                          TimeoutError)
from csti.program_view.make import MakeTarget
from csti.program_view.test_result import TestResultList, TestStatus
from csti.program_view.utils import normalizeText


class ProgramView:
    """
    Выполняет запуск, компиляцию, форматирование и
    тестирование программы на заданном языке.
    """

    def __init__(self, filePath: str, lang: Language):
        self._lang = lang
        self._filePath = filePath
        self._dir, self._file = os.path.split(filePath)
        self._fileName, self._fileExt = os.path.splitext(self._file)

    def _makeTargetCommand(self, target: MakeTarget, **kwargs) -> list[str]:
        """Возвращает команду для запуска цели в makefile."""
        return [
            "make",
            target.value,
            "-f",
            self.lang.makefile,
            *[f"{key}={value}" for key, value in kwargs.items()],
        ]

    def compile(self):
        """Компилирует программу."""

        if not self.lang.isCompiledLanguage:
            return

        result: subprocess.CompletedProcess = subprocess.run(
            self._makeTargetCommand(
                MakeTarget.compile,
                filePath=self.filePath,
            ),
            capture_output=True,
        )

        if result.returncode != 0:
            self.clear()
            raise CompileError(result.stderr.decode())

    def run(self, input: str | None = None, timeout: str | None = None) -> str:
        """
        Запускает программу и возвращает её вывод.
        Если язык компилируемый, то требуется вызов метода compile.
        """

        inputBuffer = input.encode() if input else None

        try:
            result: subprocess.CompletedProcess = subprocess.run(
                self._makeTargetCommand(
                    MakeTarget.run, filePath=self.filePath, outputFile=self._outputFile
                ),
                capture_output=True,
                input=inputBuffer,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            raise TimeoutError

        if result.returncode != 0:
            raise RunError(result.stderr.decode())

        output = ""
        with open(os.path.join(self._dir, self._outputFile), "r") as file:
            output = file.read()

        return output

    def format(self, formatStyle: str) -> Self:
        """
        Выполняет форматирование программы, возвращает экземпляр
        ProgramView для отформатированного файла.
        """

        if formatStyle not in self.lang.availableformatStyles:
            raise FormatError(
                f"Неизвестный стиль форматирование: {formatStyle} для языка {self.lang.fullName}"
            )

        result: subprocess.CompletedProcess = subprocess.run(
            self._makeTargetCommand(
                MakeTarget.format,
                filePath=self.filePath,
                formattedFile=self._formattedFile,
                formatStyle=formatStyle,
            ),
            capture_output=True,
        )

        if result.returncode != 0:
            raise FormatError(result.stderr.decode())

        formattedPath = os.path.join(self._dir, self._formattedFile)
        return ProgramView(formattedPath, self.lang)

    def clear(self, clearSelf: bool = False):
        """
        Очистка временных файлов.

        @param clearSelf: Требуется ли очистка самой программы?
        """

        subprocess.run(
            self._makeTargetCommand(
                MakeTarget.clear, filePath=self.filePath, outputFile=self._outputFile
            ),
            capture_output=True,
        )

        if clearSelf:
            os.remove(self.filePath)

    # TODO: добавить ограничение занимаемой памяти при выполнении теста.
    def test(
        self,
        testCases: list[tuple[str, str]],
        timeLimit: int | None = None,
        memoryLimit: int | None = None,
    ) -> TestResultList:
        """
        Запуск тестов. Если язык компилируемый, то требуется вызов метода compile.

        @param testCases: [(вход, ожидаемый выход), ...].
        @param timeLimit: Максимальное время в секундах для выполнения теста.
        @param memoryLimit: Максимальное количество памяти в мегабайтах для выполнения теста.
        """

        results = TestResultList()
        for input, expected in testCases:
            try:
                output = normalizeText(self.run(input, timeLimit))
                expected = normalizeText(expected)

                if output == expected:
                    results.append(TestStatus.ok)
                else:
                    results.append(
                        TestStatus.wrongAnswer,
                        input=input,
                        output=output,
                        expected=expected,
                    )
            except RunError as error:
                results.append(
                    TestStatus.runtimeError, input=input, message=error.__str__()
                )
            except TimeoutError:
                results.append(TestStatus.timeLimit, input=input)

        return results

    @property
    def filePath(self) -> str:
        return self._filePath

    @property
    def lang(self) -> Language:
        return self._lang

    @property
    def code(self) -> str:
        """Код программы."""
        with open(self.filePath, "r") as file:
            return file.read()

    @property
    def _outputFile(self) -> str:
        """Куда будут сохранены выходные данные?"""
        return self._fileName + "-out"

    @property
    def _formattedFile(self) -> str:
        """Файл после форматирования программы."""
        return self._fileName + "-fmt" + self._fileExt
