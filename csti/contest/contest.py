from csti.etc.language import Language
from csti.contest.contest_interface import ContestInterface
from csti.contest.task.task import Task
from csti.contest.exceptions import ContestException


class Contest:
	def __init__(self, id: str, taskIds: list[str], currentTaskId: str|None = None):
		if len(taskIds) == 0:
			raise ContestException("Контест должен содержать хотя бы одно задание.")

		self._tasks: dict[Task] = {taskId: Task(taskId) for taskId in taskIds}

		if currentTaskId is None:
			currentTaskId = taskIds[0]
		self._currentTaskId: str = currentTaskId

		self._id: str = id

		ContestInterface().selectContest(self._id)

	@property
	def tasks(self) -> list[Task]:
		return list(self._tasks.values())
	
	def getTask(self, id: str) -> Task:
		return self._tasks.get(id)

	def selectTask(self, taskLocalId: int):
		taskLocalId -= 1
		if taskLocalId not in range(0, len(self._tasks)):
			raise ContestException(f"Невалидный id задания: {taskLocalId}")
		self._currentTaskId = taskLocalId

	@property
	def currentTask(self) -> Task|None:
		return self._tasks.get(self._currentTaskId, None)

	@property
	def id(self) -> str:
		return self._id
	
	@property
	def lang(self) -> Language:
		langId = int(self.id[2] + "0")
		# Временно
		if langId == 50:
			return Language.nasm
		return Language.fromId(langId)
