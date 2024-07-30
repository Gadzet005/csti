import subprocess
import os
from abc import ABC, abstractmethod
from exceptions import (
    ProgramCompilerError, ProgramRunTimeError
)

class Tester(ABC):
    # Запуск программы. Возращает вывод программы
    @classmethod
    @abstractmethod
    def _runProgram(cls, path: str, input: str) -> str:
        pass
    
    # Запуск и тестирование
    @classmethod
    def testProgram(cls, path: str, input: str, expected: str):
        output = cls._runProgram(path, input).strip()
        if output!= expected:
            raise ProgramRunTimeError(f"\nОжидаемый вывод: {expected}\nПолученный: {output}")

class CTester(Tester):
    COMPILER = "gcc"
    FLAGS = [
        "-O2", "-Wall", "-Werror", "-Wformat-security", "-Wignored-qualifiers", "-Winit-self", "-Wswitch-default", "-Wfloat-equal",
        "-Wpointer-arith", "-Wtype-limits", "-Wempty-body", "-Wno-logical-op", "-Wstrict-prototypes", "-Wold-style-declaration", 
        "-Wold-style-definition", "-Wmissing-parameter-type", "-Wmissing-field-initializers", "-Wnested-externs", 
        "-Wno-pointer-sign", "-Wno-unused-result", "-std=gnu99", "-lm"
    ]

    @classmethod
    def _runProgram(cls, path: str, input: str) -> str:
        outputFilePath = os.path.join(os.path.dirname(path), "output")
        
        compileResult = subprocess.run([cls.COMPILER, *cls.FLAGS, path, "-o", outputFilePath])
        if compileResult.returncode != 0:
            raise ProgramCompilerError(f"Ошибка компиляции файла '{path}'")

        result = subprocess.run([outputFilePath], input=input.encode(), capture_output=True)

        return result.stdout.decode()

CTester.testProgram("/home/gadzet/my/main.c", "1 4", "5")