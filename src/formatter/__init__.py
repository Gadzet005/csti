import os
import subprocess
from src.consts import Language
from src.formatter.exceptions import FormatNotSupported, FormatError


class Formatter:
    def __init__(self, lang: Language, path: str):
        if not self.canBeFormatted(lang):
            raise FormatNotSupported(lang)
        self._makefile = self.getMakefileByLang(lang)

        self._dir, self._file = os.path.split(path)
        self._fileName, self._fileExt = os.path.splitext(self._file)

    @staticmethod
    def getMakefileByLang(lang: Language):
        match lang:
            case Language.c:
                return "src/formatter/make/c"
            case Language.cpp:
                return "src/formatter/make/c"
            case _:
                return None
    
    # Поддерживается ли форматирование языка
    @classmethod
    def canBeFormatted(cls, lang: Language):
        return cls.getMakefileByLang(lang) is not None
    
    @property
    def _formattedFileName(self):
        return self._fileName + "-formatted" + self._fileExt

    # Форматирует указанный файл и возвращает путь до отформатированного файла
    def format(self):
        formatted = self._formattedFileName
        result = subprocess.run(
            [
                "make", "format", "-f", self._makefile, f"DIR={self._dir}", 
                f"FILE={self._file}", f"FORMATTED_FILE={formatted}"
            ],
            capture_output=True
        )

        if result.returncode != 0:
            raise FormatError(
                f"Ошибка при форматировании файла '{self._file}':\n{result.stderr.decode()}"
            )

        return os.path.join(self._dir, formatted)
    
    # Очищает отформатированный файл
    def clear(self):
        subprocess.run([
            "make", "clear", "-f", self._makefile, 
             f"DIR={self._dir}", f"FORMATTED_FILE={self._formattedFileName}"
        ], capture_output=True)