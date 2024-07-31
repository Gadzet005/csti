from .task_status_info import TaskStatusInfo
from .contest_interface import ContestInterface
from .parser import Parser


# TODO: Добавить кеширование и проверку возвращаемого значения в функциях.
class Task:
	def __init__(self, contestInterface: ContestInterface, id_: int) -> None:
		self._contestInterface: ContestInterface = contestInterface
		self._id: int = id_
	
	@property
	def _html(self) -> bytes:
		return self._contestInterface.requestTask(self._id).content

	@property
	def info(self) -> map:
		return Parser.getTaskInfo(self._html)

	@property
	def name(self) -> str:
		return Parser.getTaskName(self._html)

	@property
	def condition(self) -> str:
		return Parser.getTaskCondition(self._html)

	@property
	def tests(self) -> zip:
		return Parser.getTaskTests(self._html)

	@property
	def status(self) -> TaskStatusInfo|None:
		return Parser.getLastStatus(self._html)

	def sendSolution(self, file: str):
		return self._contestInterface.sendTask(self._id, file)

