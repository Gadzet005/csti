from .contest_interface import ContestInterface
from .parser import Parser

from bs4 import BeautifulSoup

class Task:
	def __init__(self, contestInterface: ContestInterface, id_: int) -> None:
		self._contestInterface: ContestInterface = contestInterface
		self._id: int = id_
	
	@property
	def _getHtml(self) -> bytes:
		return self._contestInterface.requestTask(self._id).content

	@property
	def getInfo(self):
		return

	@property
	def getName(self):
		return Parser.getTaskName(self._getHtml)
		

	@property
	def getCondition(self):
		return Parser.getTaskCondition(self._getHtml)

	@property
	def getTests(self):
		return Parser.getTaskTests(self._getHtml)

	@property
	def getStatus(self):
		pass

	def sendSolution(self, file: str):
		return self._contestInterface.sendTask(self._id, file)

