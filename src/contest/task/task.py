from src.contest.contest_interface import ContestInterface
from src.contest.parser.task_parser import TaskParser
from src.contest.task.solution import Solution


# TODO: Добавить кеширование и проверку возвращаемого значения в функциях.
class Task:
	def __init__(self, contestInterface: ContestInterface, id_: int) -> None:
		self._contestInterface: ContestInterface = contestInterface
		self._id: int = id_
	
	def _getHtml(self) -> bytes:
		return self._contestInterface.requestTask(self._id).content

	def getInfo(self) -> map:
		return TaskParser.getInfo(self._getHtml())

	def getName(self) -> str:	
		return TaskParser.getName(self._getHtml())

	def getCondition(self) -> str:
		return TaskParser.getCondition(self._getHtml())

	def getTests(self) -> zip:
		return TaskParser.getTests(self._getHtml())

	def getStatus(self) -> Solution|None:
		return TaskParser.getLastSolution(self._getHtml())

	def sendSolution(self, file: str):
		return self._contestInterface.sendTask(self._id, file)

