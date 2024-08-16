from enum import Enum


class Locale(Enum):
    english = 0
    russian = 1
    ukrainian = 2
    kazakh = 3


class Language(Enum):
    c = 1 # TODO: найти id для c и c++
    cpp = 2
    asm = 50


class ContestConsts(object):
	URL = "https://contest.solutions"
	NON_AUTHENTICATED_SESSION_ID = "0000000000000000"
	
	@staticmethod
	def getRequestsUrl():
		return f"{ContestConsts.URL}/cgi-bin/new-client"

# TODO: Не работает если в ссылке ошибка.
REQUEST_TIME_LIMIT = 10 
PARSER_TYPE = "html.parser"


NO_CONTEST_SUPPORT = "Не поддерживаемый контест"
