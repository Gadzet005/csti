from bs4 import BeautifulSoup
import re
import requests
from inspect import cleandoc


from .task_status_info import TaskStatusInfo
from .exceptions import ParserException

from src.login import HOME_URL, FIO_PATERN


PARSER_TYPE = "html.parser"

# TODO: Добавить кэширование.

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

	# TODO: Нормальный возвращаемый тип данных.
	@staticmethod
	def getTaskInfo(html: bytes) -> map:
		soup = BeautifulSoup(html, PARSER_TYPE)
		infoContainer = soup.find("table", class_="line-table-wb")
		if infoContainer is None:
			raise ParserException("Ошибка при получении информации о задачи")
		
		infoStrings = cleandoc(infoContainer.text).split("\n")
		info = map(
			lambda infoString: tuple(infoString.split(":")),
			infoStrings
		)

		return info

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
			lambda element: cleandoc(element.text),
			conditionElements)
		)

		return cleandoc(condition)


	# TODO: Нормальный возвращаемый тип данных.
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

	@staticmethod
	def getLastStatus(html: bytes) -> TaskStatusInfo|None:
		soup = BeautifulSoup(html, PARSER_TYPE)
		statusTable = soup.find("table", class_="table")
		if statusTable is None:
			return None
		statusHistoryLine = statusTable.find_all("tr")
		if statusHistoryLine is None:
			raise ParserException("Ошибка при получении статуса задачи.")
		# Не учитываем строку с информацией о колоннах
		statusBlocks = statusHistoryLine[1].find_all("td", class_="b1")
		if statusBlocks is None:
			raise ParserException("Ошибка при получении статуса задачи.")
		
		return TaskStatusInfo(
			int(statusBlocks[0].text),
			statusBlocks[4].text,
			int(statusBlocks[5].text)
		)

	@staticmethod
	def getHwContestIdAndUserTasks(localContestId: int) -> tuple[int, map]:
		response = requests.get(HOME_URL)
		soup = BeautifulSoup(response.content, PARSER_TYPE)
		tabcontent = soup.find("div", id=f"block_hw{localContestId}")
		if tabcontent is None:
			raise ParserException("Не удалось получить список заданных задач или номер контеста.")
		
		
		contestButton = tabcontent.find("a", class_="button")
		if contestButton is None:
			raise ParserException("Не удалось получить номер контеста.")

		contestIdMatches = re.findall(r"Контест (\d{4})", contestButton.text)

		if contestIdMatches is None or len(contestIdMatches) != 1:
			raise ParserException("Не удалось получить номер контеста.")

		contestId = int(contestIdMatches[0])

		if contestButton is None:
			raise ParserException("Не удалось получить номер контеста.")

		homeworksMathes = tabcontent.find_all("td", string=re.compile(FIO_PATERN))

		if homeworksMathes is None or len(homeworksMathes) != 1:
			raise ParserException("Не удалось получить список задач проверьте паттерн ФИО.")
		tasks = homeworksMathes[0].parent.find_all(string=re.compile(r"\d"))

		"""
		TODO: В некоторых задачах есть буквы, написать норм решение.
		Пример: R = 10
		"""
		tasks = map(lambda task: task.replace("R", "10"), tasks)
		return (contestId, tasks)

	@staticmethod
	def getAviableHwContestsCount() -> int:
		response = requests.get(HOME_URL)
		soup = BeautifulSoup(response.content, PARSER_TYPE)
		nav = soup.find("nav")
		if nav is None:
			raise ParserException("Не удалось получить кол-во контестов")

		hwContestButtons = nav.find_all("a", href=re.compile(r"#hw\d+"))
		
		if hwContestButtons is None:
			raise ParserException("Не удалось получить кол-во контестов")

		return len(hwContestButtons)
