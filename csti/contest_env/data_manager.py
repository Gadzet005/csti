from __future__ import annotations

import os

from csti.consts import APP_NAME
from csti.cli.exceptions import DataManagerException
from csti.contest import Contest


class DataManager:
	FOLDER = "." + APP_NAME
	ARRAY_SEPARATOR = ", "

	groups = {
		"contest":			"contest"
	}

	vars = {
		"contestId":		os.path.join(groups.get("contest"), "id"),
		"tasksId":			os.path.join(groups.get("contest"), "taskId"),
		"selectedTaskId":	os.path.join(groups.get("contest"), "selectedTaskId"),
	}

	def __init__(self, dir: str):
		self._dir = dir

	@staticmethod
	def create(dir: str) -> DataManager:
		for groupDir in DataManager.groups.values():
			os.makedirs(os.path.join(dir, groupDir), exist_ok=True)
		return DataManager(dir)
	
	def _getVarPath(self, name: str):
		return os.path.join(self._dir, self.vars[name])

	def saveContest(
			self, 
			id: str|None = None, 
			tasksId: list[str]|None = None, 
			taskLocalId: str = "1"
		):
		try:
			if id:
				with open(self._getVarPath("contestId"), "w") as file:
					file.write(id)

			if tasksId:
				with open(self._getVarPath("tasksId"), "w") as file:
					file.write(DataManager.ARRAY_SEPARATOR.join(tasksId))

			with open(self._getVarPath("selectedTaskId"), "w") as file:
				file.write(taskLocalId)
		except FileNotFoundError as error:
			raise DataManagerException(
				f"Директории не существует: '{os.path.dirname(error.filename)}'."
			)

	def loadContest(self) -> Contest:
		try:
			with open(self._getVarPath("contestId"), "r") as file:
				id = file.read()
			with open(self._getVarPath("tasksId"), "r") as file:
				tasksId = file.read().split(DataManager.ARRAY_SEPARATOR)
			with open(self._getVarPath("selectedTaskId"), "r") as file:
				selectedTaskId = int(file.read())
		except FileNotFoundError as error:
			raise DataManagerException(f"Файл не существует: '{error.filename}'.")
	
		contest = Contest(id, tasksId)
		contest.selectTask(selectedTaskId)
		
		return contest
