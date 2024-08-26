from __future__ import annotations

from enum import Enum

APP_NAME = "csti"


class ContestConsts:
	URL = "https://contest.solutions"
	PARSER_TYPE = "html.parser"
	NON_AUTHENTICATED_SESSION_ID = "0000000000000000"
	
	@staticmethod
	def getRequestsUrl() -> str:
		return f"{ContestConsts.URL}/cgi-bin/new-client"


class CliConsts:
	NO_CONTEST_SUPPORT = "Не поддерживаемый контест"


class Locale(Enum):
	english = 0
	russian = 1
	ukrainian = 2
	kazakh = 3


class Language(Enum):
	# TODO: добавить все возможные языки
	c = 1 # TODO: найти id для c и c++
	cpp = 2
	asm = 50

	@staticmethod
	def fromName(lang: str) -> Language|None:
		try:
			return Language[lang]
		except KeyError:
			return None
