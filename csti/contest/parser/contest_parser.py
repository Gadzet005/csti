import re

from bs4 import BeautifulSoup

from consts import ContestConsts
from contest.exceptions import CantParseElement
from contest.task.solution import SolutionStatus


class ContestParser(object):
	@staticmethod
	def getSessionId(html: bytes) -> str:
		soup = BeautifulSoup(html, ContestConsts.PARSER_TYPE)
		script = soup.find("script", string=re.compile("var SID="))
		if script is None:
			raise CantParseElement("script")
		
		sessionIdMatches = re.findall(r'var SID="(\w{16})"', script.text)
		if len(sessionIdMatches) != 1:
			raise CantParseElement("session id")
		
		return sessionIdMatches[0]

	"""
		 Если тип дз не является контестом то возвращается -1.
	"""
	@staticmethod
	def getHomework(html: bytes, namePattern: str, localContestId: int) \
		-> tuple[str, list[tuple[str, SolutionStatus]]]:
		
		soup = BeautifulSoup(html, ContestConsts.PARSER_TYPE)
		tabcontent = soup.find("div", id=f"block_hw{localContestId}")
		if tabcontent is None:
			raise CantParseElement("tabcontent") 
		
		contestButton = tabcontent.find("a", class_="button")
		if contestButton is None:
			raise CantParseElement("contestButton") 

		contestIdMatches = re.findall(r"Контест (\d{4})", contestButton.text)
		if contestIdMatches is not None and len(contestIdMatches) == 1:
			contestId = contestIdMatches[0]
		else:
			contestId = "-1"

		homeworksMathes = tabcontent.find_all("td", string=re.compile(namePattern))
		if homeworksMathes is None or len(homeworksMathes) != 1:
			raise CantParseElement("homework")
		
		tasks = list()
		for taskId in homeworksMathes[0].parent.find_all(string=re.compile(r"\d")):
			task = (taskId, SolutionStatus.unclassified_error)
			tasks.append(task)

		return (contestId, tasks)
	
	@staticmethod
	def getAvailableHomeworkCount(html: bytes) -> int:
		soup = BeautifulSoup(html, ContestConsts.PARSER_TYPE)
		nav = soup.find("nav")
		if nav is None:
			raise CantParseElement("nav")

		hwContestButtons = nav.find_all("a", href=re.compile(r"#hw\d+"))
		if hwContestButtons is None:
			raise CantParseElement("hwContestButtons")

		return len(hwContestButtons)
