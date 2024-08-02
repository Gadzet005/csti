"""
	Шаблон файла конфигурации.
	Чтобы активировать переименуйте в config.py.
"""

from src.consts import Language, Locale

LOCALE = Locale.russian.value
LANG_ID = Language.asm

"""
	Страница с номерами заданых задач.
	Note: Удалите все что идет после группы.
"""
HOME_URL = "https://contest.solutions/msu/102"

login = ""
password = ""
FIO_PATERN = r"ФАМИЛИЯ\w*"
