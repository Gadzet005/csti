from csti.consts import Language
from csti.contest.contest_interface import ContestInterface
from csti.contest.task.task import Task
from csti.contest.exceptions import ContestException


class Contest:
	def __init__(self, id: str, tasksId: list[str]):
		self._tasks: list[Task] = list()
		for taskId in tasksId:
			self._tasks.append(Task(taskId))

		self._curentTaskLocalId: int = 0
		self._id: str = id

		ContestInterface().selectContest(self._id)

	@property
	def tasks(self) -> list[Task]:
		return self._tasks

	def selectTask(self, taskLocalId: int):
		taskLocalId -= 1
		if taskLocalId not in range(0, len(self._tasks)):
			raise ContestException(f"Невалидный id задания: {taskLocalId}")
		self._curentTaskLocalId = taskLocalId

	@property
	def currentTask(self) -> Task:
		return self._tasks[self._curentTaskLocalId]

	@property
	def id(self) -> str:
		return self._id
	
	@property
	def lang(self) -> Language:
		langId = int(self.id[2] + "0")
		return Language.fromId(langId)
