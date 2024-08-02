import os
from enum import Enum

from src.consts import Language
from src.program.exceptions import UnexpectedLanguage


class MakeInfo:
    MAKE_DIR = "src/program/make"
    FORMAT_CONFIGS_DIR = "src/program/format_configs"

    class Target(Enum):
        compile = "compile"
        run = "run"
        clear = "clear"
        format = "format"

    def __init__(self, lang: Language):
        self._makefile: str|None = None
        self._canBeCompiled: bool = True
        self._canBeFormatted: bool = True
        self._formatConfig: str|None = None

        match lang:
            case Language.c:
                self._makefile = os.path.join(self.MAKE_DIR, "c")
                self._formatConfig = os.path.join(self.FORMAT_CONFIGS_DIR, "cformat.yaml")
            case Language.cpp:
                self._makefile = os.path.join(self.MAKE_DIR, "cpp")
                self._formatConfig = os.path.join(self.FORMAT_CONFIGS_DIR, "cformat.yaml")
            case Language.asm:
                self._makefile = os.path.join(self.MAKE_DIR, "asm")
                self._canBeFormatted = False
            case _:
                raise UnexpectedLanguage(lang)
    
    @property
    def canBeCompiled(self) -> bool:
        return self._canBeCompiled
    
    @property
    def canBeFormatted(self) -> bool:
        return self._canBeFormatted
    
    @property
    def makefile(self) -> str|None:
        return self._makefile
    
    @property
    def formatConfig(self) -> str|None:
        return self._formatConfig
