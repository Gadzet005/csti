from typing import List

from src.contest.contest_interface import ContestInterface
from src.contest.task.task import Task


class Contest:
	def __init__(self, id: str, tasksId: List[str]):
		self._tasks: List[Task] = list()
		self._curentTaskId: int = 0
		for taskId in tasksId:
			task = Task(taskId)
			self._tasks.append(task)

		self._id: str = id

		ContestInterface().selectContest(self._id)

	def getTasksId(self) -> list[str]:
		tasksId = list()
		for task in self._tasks:
			tasksId.append(task.id)
		return tasksId

	def selectTask(self, taskLocalId: int):
		taskLocalId -= 1
		if taskLocalId not in range(0, len(self._tasks)):
			raise 
		self._curentTaskId = taskLocalId

	@property
	def currentTask(self) -> Task:
		return self._tasks[self._curentTaskId]

	@property
	def id(self) -> str:
		return self._id
