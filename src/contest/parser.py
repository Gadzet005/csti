from bs4 import BeautifulSoup
import re
from inspect import cleandoc
from src.exceptions import ParserException

PARSER_TYPE = "html.parser"

class Parser(object):
	@staticmethod
	def getSessionId(html: bytes) -> str:
		soup = BeautifulSoup(html, "html.parser")
		script = soup.find("script", string=re.compile("var SID="))
		# TODO: Убрать повторения.
		if script is None:
			raise ParserException("Ошибка при парсинге SID.")
		sessionIdMatches = re.findall(r'var SID="(\w{16})"', script.text)

		if len(sessionIdMatches) != 1:
			raise ParserException("Ошибка при парсинге SID.")
		
		return sessionIdMatches[0]

	@staticmethod
	def getTaskName(html: bytes) -> str:
		soup = BeautifulSoup(html, PARSER_TYPE)
		nameElement = soup.find("h3")
		if nameElement is None:
			raise ParserException("Ошибка при получении имени задачи.")
		
		return nameElement.text

	@staticmethod
	def getTaskCondition(html: bytes) -> str:
		soup = BeautifulSoup(html, PARSER_TYPE)
		taskContainer = soup.find("div", id="probNavTaskArea-ins")
		if taskContainer is None:
			raise ParserException("Ошибка при получении условия задачи.")
		conditionElements = taskContainer.find_all("p", recursive=False)
		if conditionElements is None:
			raise ParserException("Ошибка при получении условия задачи.")
	
		# TODO: Испривать форматирование(также перевод в текст сейчас 10^9 = 109 = 10_9)
		condition = "".join(map(
			lambda element: element.text,
			conditionElements)
		)

		return cleandoc(condition)

	@staticmethod
	def getTaskTests(html: bytes) -> zip:
		soup = BeautifulSoup(html, PARSER_TYPE)
		testsElements = soup.find_all("pre")
		if testsElements is None:
			# TODO: Может быть это предупреждение?
			raise ParserException("Ошибка при получении тестов задачи")
		
		testsUnparse = map(lambda testElement: testElement.text, testsElements)
		testsIterator = iter(testsUnparse)
		return zip(testsIterator, testsIterator)

