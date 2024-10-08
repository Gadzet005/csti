from __future__ import annotations

import os
import subprocess
import typing as t

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

    def run(
        self, input: t.Optional[str] = None, timeLimit: t.Optional[float] = None
    ) -> str:
        """
        Запускает программу и возвращает её вывод.
        Если язык компилируемый, то требуется вызов метода compile.
        """

        inputBuffer = input.encode() if input else None

        try:
            result: subprocess.CompletedProcess = subprocess.run(  # type: ignore
                self._makeTargetCommand(
                    MakeTarget.run, filePath=self.filePath, outputFile=self._outputFile
                ),
                capture_output=True,
                input=inputBuffer,
                timeout=timeLimit,
            )
        except subprocess.TimeoutExpired:
            raise TimeoutError

        if result.returncode != 0:
            raise RunError(result.stderr.decode())

        output = ""
        with open(os.path.join(self._dir, self._outputFile), "r") as file:
            output = file.read()

        return output

    def format(
        self, formatStyle: str, formattedPath: t.Optional[str] = None
    ) -> ProgramView:
        """
        Выполняет форматирование программы, возвращает экземпляр
        ProgramView для отформатированного файла.

        :param formatStyle:
            Стиль форматирования, который будет применен к файлу.
            Должен быть в атрибуте `availableformatStyles` в языке программы.
        :param formatFilePath:
            Путь до отформатированного файла. Если `None`,
            то форматированный файл добавляется в
            ту же папку с названием по умолчанию.
        """

        if formatStyle not in self.lang.availableformatStyles:
            raise FormatError(
                f"Неизвестный стиль форматирование: {formatStyle} для языка {self.lang.fullName}"
            )

        formattedPath = formattedPath or self._defaultformattedPath

        result: subprocess.CompletedProcess = subprocess.run(
            self._makeTargetCommand(
                MakeTarget.format,
                filePath=self.filePath,
                formattedPath=formattedPath,
                formatStyle=formatStyle,
            ),
            capture_output=True,
        )

        if result.returncode != 0:
            raise FormatError(result.stderr.decode())

        return ProgramView(formattedPath, self.lang)

    def clear(self, clearSelf: bool = False):
        """
        Очистка временных файлов.

        :param clearSelf: Требуется ли очистка самой программы?
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
        timeLimit: t.Optional[float] = 1.0,
        memoryLimit: t.Optional[float] = None,
    ) -> TestResultList:
        """
        Запуск тестов. Если язык компилируемый, то требуется вызов метода compile.

        :param testCases: [(вход, ожидаемый выход), ...].
        :param timeLimit:
            Максимальное время в секундах для выполнения теста.
            Если `None`, то время не ограничено.
        :param memoryLimit:
            Максимальное количество памяти в мегабайтах для выполнения теста.
            Если `None`, то память не ограничена.
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
    def _defaultformattedPath(self) -> str:
        """Путь до отформатированного файла по умолчанию."""
        return os.path.join(self._dir, self._fileName + "-fmt" + self._fileExt)
