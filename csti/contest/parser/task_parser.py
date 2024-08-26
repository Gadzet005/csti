from inspect import cleandoc

from bs4 import BeautifulSoup

from csti.consts import ContestConsts
from csti.contest.exceptions import CantParseElement
from csti.contest.task.solution import Solution, SolutionStatus


class TaskParser(object):
	@staticmethod
	def getName(html: bytes) -> str:
		soup = BeautifulSoup(html, ContestConsts.PARSER_TYPE)
		nameElement = soup.find("h3")
		if nameElement is None:
			raise CantParseElement("name")
		
		return nameElement.text

	@staticmethod
	def getInfo(html: bytes) -> dict[str, str]:
		soup = BeautifulSoup(html, ContestConsts.PARSER_TYPE)
		infoContainer = soup.find("table", class_="line-table-wb")
		if infoContainer is None:
			raise CantParseElement("info") 
		
		infoStrings = cleandoc(infoContainer.text).split("\n")
		info = dict(map(
			lambda infoString: tuple(infoString.split(":", 1)),
			infoStrings
		))

		return info

	@staticmethod
	def getCondition(html: bytes) -> str:
		soup = BeautifulSoup(html, ContestConsts.PARSER_TYPE)
		taskContainer = soup.find("div", id="probNavTaskArea-ins")
		if taskContainer is None:
			raise CantParseElement("condition")
		
		conditionElements = taskContainer.find_all("p", recursive=False)
		if conditionElements is None:
			raise CantParseElement("condition")
	
		# TODO: Испривать форматирование(также перевод в текст сейчас 10^9 = 109 = 10_9)
		condition = "".join(map(
			lambda element: cleandoc(element.text).replace("\n", " "),
			conditionElements)
		)

		return cleandoc(condition)

	@staticmethod
	def getTests(html: bytes) -> list[tuple[str, str]]:
		soup = BeautifulSoup(html, ContestConsts.PARSER_TYPE)
		testsElements = soup.find_all("pre")
		if testsElements is None:
			raise CantParseElement("tests")
		
		testsUnparse = map(lambda testElement: testElement.text, testsElements)
		testsIterator = iter(testsUnparse)
		
		return list(zip(testsIterator, testsIterator))

	@staticmethod
	def getLastSolution(html: bytes) -> Solution|None:
		soup = BeautifulSoup(html, ContestConsts.PARSER_TYPE)
		statusTable = soup.find("table", class_="table")
		if statusTable is None:
			return None
		
		statusHistoryLine = statusTable.find_all("tr")
		if statusHistoryLine is None:
			raise CantParseElement("last solution")
		
		# Не учитываем строку с информацией о колоннах
		statusBlocks = statusHistoryLine[1].find_all("td", class_="b1")
		if statusBlocks is None:
			raise CantParseElement("last solution")

		testPassedElement = statusBlocks[5].text

		
		
		return Solution(
			int(statusBlocks[0].text),
			SolutionStatus(statusBlocks[4].text),
			int(testPassedElement if testPassedElement.isdigit() else 0)
		)

