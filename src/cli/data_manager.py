import os

from src.cli.exceptions import DataManagerException
from src.consts import APP_NAME
from src.contest.contest import Contest

ARRAY_SEPARATOR = ", "

class DataManager:
	dirs = {
		"contest":              f".{APP_NAME}/contest/"
	}

	paths = {
		"contestId":            f"{dirs['contest']}/id",
		"tasksId":              f"{dirs['contest']}/taskId",
		"selectedTaskLocalId":  f"{dirs['contest']}/selectedTaskLocalId"
	}

	@staticmethod
	def init():
		for dir in DataManager.dirs.values():
			os.makedirs(os.path.dirname(dir), exist_ok=True)

	@staticmethod
	def saveContest(id: str|None = None, tasksId: list[str]|None = None, taskLocalId: str = "1"):
		for dir in DataManager.dirs.values():
			isDirExsist = os.path.exists(dir)
			if isDirExsist == False:
				raise DataManagerException(f"Не проинициализированны директории: {dir}.")

		if id:
			with open(DataManager.paths["contestId"], "w") as file:
				file.write(id)

		if tasksId:
			with open(DataManager.paths["tasksId"], "w") as file:
				file.write(ARRAY_SEPARATOR.join(tasksId))

		with open(DataManager.paths["selectedTaskLocalId"], "w") as file:
			file.write(taskLocalId)

	@staticmethod
	def loadContest() -> Contest:
		for path in DataManager.paths.values():
			isFileExsist = os.path.exists(path)
			if isFileExsist == False:
				raise DataManagerException(f"Не проинициализированны данные: {path}.")
		

		with open(DataManager.paths["contestId"], "r") as file:
			id = file.read()
		with open(DataManager.paths["tasksId"], "r") as file:
			tasksId = file.read().split(ARRAY_SEPARATOR)
		with open(DataManager.paths["selectedTaskLocalId"], "r") as file:
			selectedTaskLocalId = int(file.read())
		
		contest = Contest(id, list(tasksId))
		contest.selectTask(selectedTaskLocalId)
		
		return contest


