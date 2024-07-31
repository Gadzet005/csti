from .contest_interface import ContestInterface
from .parser import Parser


class Task:
	def __init__(self, contestInterface: ContestInterface, id_: int) -> None:
		self._contestInterface: ContestInterface = contestInterface
		self._id: int = id_
	
	@property
	def _html(self) -> bytes:
		return self._contestInterface.requestTask(self._id).content

	@property
	def info(self):
		return

	@property
	def name(self):
		return Parser.getTaskName(self._html)

	@property
	def condition(self):
		return Parser.getTaskCondition(self._html)

	@property
	def tests(self):
		return Parser.getTaskTests(self._html)

	@property
	def status(self):
		pass

	def sendSolution(self, file: str):
		return self._contestInterface.sendTask(self._id, file)

