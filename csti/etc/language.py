import enum
import typing as t

from csti.etc.consts import BASE_DIR


class Language(enum.Enum):
    """
    Интерфейс перечисления языков программирования.
    -----------------------------------------------
    Атрибуты члена перечисления:
    - id (`int`):								Идентификатор.
    - fullName (`str`):							Название.
    - isCompiledLanguage (`bool`):				Яввляется ли компилируемым языком?

    - availableFileExtensions (`list[str]`):    Доступные расширения файла.
        - Первое расширение в списке используется по умолчанию.
        - Расширения используется вместе с точкой: `.py`, `.cpp`.

    - comment (`str`):                          Символ комментария.
    - makefile (`str`):                         Пусть к makefile для работы с программой.

    - availableformatStyles (`list[str]`):      Доступные стили форматирования.
        - Если атрибута нет, то форматирование для программ с этим языком не доступно.

    - templateFile (`str` | `None`)             Путь до шаблонного файла.
        - Если `None`, то шаблонного файла нет (Если атрибута нет, то считаем, что `None`).
    """

    @classmethod
    def fromName(cls, name: str) -> t.Optional[t.Self]:
        """Получить язык по имени. Возвращает None, если такого нет."""
        try:
            return cls[name]
        except KeyError:
            return None

    @classmethod
    def fromId(cls, id: int) -> t.Optional[t.Self]:
        """Получить язык по id. Возвращает None, если такого нет."""
        for lang in cls:
            if lang.id == id:
                return lang
        return None

    @property
    def id(self) -> int:
        return self.value["id"]

    @property
    def fullName(self) -> str:
        return self.value["fullName"]

    @property
    def isCompiledLanguage(self) -> bool:
        return self.value["isCompiledLanguage"]

    @property
    def availableFileExtensions(self) -> list[str]:
        return self.value["availableFileExtensions"]

    @property
    def defaultfileExtension(self) -> str:
        return self.availableFileExtensions[0]

    @property
    def comment(self) -> str:
        return self.value["comment"]

    @property
    def makefile(self) -> str:
        return BASE_DIR / self.value["makefile"]

    @property
    def availableformatStyles(self) -> list[str]:
        return self.value.get("availableformatStyles", [])

    @property
    def templateFile(self) -> t.Optional[str]:
        template = self.value.get("templateFile", None)
        if template is None:
            return None
        return BASE_DIR / template


class GeneralLanguage(Language):
    """Перечисление языков программирования, содержащее общую информацию о них."""

    c = {
        "id": 1,
        "fullName": "C",
        "isCompiledLanguage": True,
        "availableFileExtensions": [".c"],
        "comment": "//",
        "makefile": "csti/etc/langs/c/makefile",
        "availableformatStyles": ["msu-style"],
        "templateFile": "csti/etc/langs/c/template.c",
    }

    cpp = {
        "id": 2,
        "fullName": "C++",
        "isCompiledLanguage": True,
        "availableFileExtensions": [".cpp", ".cxx"],
        "comment": "//",
        "makefile": "csti/etc/langs/cpp/makefile",
        "availableformatStyles": ["msu-style"],
        "templateFile": "csti/etc/langs/cpp/template.cpp",
    }
