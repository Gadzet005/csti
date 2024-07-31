from enum import Enum

BASE_URL = "https://contest.solutions"

class Locale(Enum):
    english = 0
    russian = 1
    ukrainian = 2
    kazakh = 3

DEFAULT_LOCALE = Locale.russian.value

class Contest(Enum):
    hse_asm_3 = 1852
    msu_asm_3 = 1752

class Language(Enum):
    c = 1 # TODO: найти id для c и c++
    cpp = 2
    asm = 50