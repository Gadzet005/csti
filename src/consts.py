from enum import Enum


class Locale(Enum):
    english = 0
    russian = 1
    ukrainian = 2
    kazakh = 3


class TaskStatus(Enum):
	accepted_for_review = "Принято на проверку"
	wrang_answer = "Неправильный ответ"
	compilation_error = "Ошибка компиляции"
	execution_error = "Ошибка выполнения"
	bad_output_format = "Неправильный формат вывода"
	unclassified_error = "Не классифицированная ошибка"


class ContestId(Enum):
    hse_asm_3 = 1852
    msu_asm_3 = 1752


class Language(Enum):
    asm = 50


BASE_URL = "https://contest.solutions"
NO_AUTH_SID = "0000000000000000"
DEFAULT_REQUESTS_URL = f"{BASE_URL}/cgi-bin/new-client"
DEFAULT_LOCALE = Locale.russian.value
DEFAULT_LANG_ID = Language.asm
