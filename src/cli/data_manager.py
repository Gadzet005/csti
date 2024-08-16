import os

from src.contest.contest import Contest

ARRAY_SEPARATOR = ", "

class DataManager:
	programmDirectory = ".csti"
	contestDirectory =              f"{programmDirectory}/contest"
	contestIdPath =		            f"{contestDirectory}/id"
	contestTasksIdPath =            f"{contestDirectory}/tasksId"
	contestSelectedTaskLocalIdPath = f"{contestDirectory}/selectedTaskLocalId"

	@staticmethod
	def saveContest(id: str|None = None, tasksId: list[str]|None = None, taskLocalId: str = "1"):
		os.makedirs(os.path.dirname(DataManager.contestIdPath), exist_ok=True)
		os.makedirs(os.path.dirname(DataManager.contestTasksIdPath), exist_ok=True)
		os.makedirs(os.path.dirname(DataManager.contestSelectedTaskLocalIdPath), exist_ok=True)

		if id:
			with open(DataManager.contestIdPath, "w") as file:
				file.write(id)

		if tasksId:
			with open(DataManager.contestTasksIdPath, "w") as file:
				file.write(ARRAY_SEPARATOR.join(tasksId))

		with open(DataManager.contestSelectedTaskLocalIdPath, "w") as file:
			file.write(taskLocalId)

	@staticmethod
	def loadContest() -> Contest:
		with open(DataManager.contestIdPath, "r") as file:
			id = file.read()
		with open(DataManager.contestTasksIdPath, "r") as file:
			tasksId = file.read().split(ARRAY_SEPARATOR)
		with open(DataManager.contestSelectedTaskLocalIdPath, "r") as file:
			selectedTaskLocalId = int(file.read())
		
		contest = Contest(id, list(tasksId))
		contest.selectTask(selectedTaskLocalId)
		
		return contest


