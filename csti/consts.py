from __future__ import annotations

import enum

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
		"canBeFormatted": True,
	}

	cpp = {
		"id": 2, # Заглушка
		"fullName": "C++",
		"fileExtension": ".cpp",
		"comment": "//",
		"canBeCompiled": True,
		"canBeFormatted": True,
	}

	asm = {
		"id": 50,
		"fullName": "Assembler x86",
		"fileExtension": ".asm",
		"comment": ";",
		"canBeCompiled": True,
		"canBeFormatted": False,
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
		return self.value["canBeFormatted"]
