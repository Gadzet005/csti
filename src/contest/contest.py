from typing import List

from src.contest.contest_interface import ContestInterface
from src.contest.task.task import Task


class Contest:
	def __init__(self, id: int, tasksId: List[int]):
		self._tasks: List[Task] = list()
		self._curentTaskId: int = 0
		for taskId in tasksId:
			task = Task(taskId)
			self._tasks.append(task)

		self._id = id

		ContestInterface().selectContest(self._id)

	def selectTask(self, taskLocalId: int):
		taskLocalId -= 1
		if taskLocalId not in range(0, len(self._tasks)):
			raise 
		self._curentTaskId = taskLocalId

	def getTask(self):
		return self._tasks[self._curentTaskId]
