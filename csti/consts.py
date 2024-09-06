from __future__ import annotations

import os
import enum

APP_NAME = "csti"
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class ContestConsts:
	URL = "https://contest.solutions"
	PARSER_TYPE = "html.parser"
	NON_AUTHENTICATED_SESSION_ID = "0000000000000000"
	
	@staticmethod
	def getRequestsUrl() -> str:
		return f"{ContestConsts.URL}/cgi-bin/new-client"


class CliConsts:
	NO_CONTEST_SUPPORT = "Не поддерживаемый контест"


@enum.unique
class Locale(enum.IntEnum):
	english = 0
	russian = 1
	ukrainian = 2
	kazakh = 3


class Language(enum.Enum):
	""" Перечисление языков программирования. """
	# TODO: добавить все возможные языки.

	c = {
		"id": 1, # Заглушка
		"fullName": "C",
		"fileExtension": ".c",
		"comment": "//",
		"canBeCompiled": True,
		"makefile": "csti/program/make/c/makefile",
		"formatConfig": "csti/program/format_configs/cformat.yaml",
	}

	cpp = {
		"id": 2, # Заглушка
		"fullName": "C++",
		"fileExtension": ".cpp",
		"comment": "//",
		"canBeCompiled": True,
		"makefile": "csti/program/make/cpp/makefile",
		"formatConfig": "csti/program/format_configs/cformat.yaml",
	}

	asm = {
		"id": 50,
		"fullName": "Assembler x86",
		"fileExtension": ".asm",
		"comment": ";",
		"canBeCompiled": True,
		"makefile": "csti/program/make/asm/makefile",
		"formatConfig": None,
	}

	@staticmethod
	def fromName(name: str) -> Language|None:
		""" Получить язык по имени. Возвращает None, если такого нет. """
		try:
			return Language[name]
		except KeyError:
			return None
	
	@staticmethod
	def fromId(id: int) -> Language|None:
		""" Получить язык по id. Возвращает None, если такого нет. """
		for lang in Language:
			if lang.id == id:
				return lang
		return None
	
	@property
	def id(self):
		""" id языка на contest.solutions. """
		return self.value["id"]

	@property
	def fullName(self) -> str:
		""" Полное назание языка. """
		return self.value["fullName"]
	
	@property
	def fileExtension(self) -> str:
		""" 
		Расширение файла, которое используется для 
		программ на этом языке. Например: ".py".
		"""
		return self.value["fileExtension"]

	@property
	def comment(self) -> str:
		""" Символы, которые используются для комментариев. """
		return self.value["comment"]

	@property
	def canBeCompiled(self) -> bool:
		""" Компилируемый ли язык? """
		return self.value["canBeCompiled"]

	@property
	def canBeFormatted(self) -> bool:
		""" Доступно ли форматирование? """
		return self.value["formatConfig"] is not None
	
	@property
	def makefile(self) -> str:
		""" Путь к makefile. """
		return os.path.join(BASE_DIR, self.value["makefile"])

	@property
	def formatConfig(self) -> str|None:
		""" Путь к конфигу для форматирования. """
		return os.path.join(BASE_DIR, self.value["formatConfig"])
