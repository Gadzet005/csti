import click
import os
from InquirerPy import inquirer

from src.config import namePattern
from src.contest.contest import Contest
from src.contest.contest_interface import ContestInterface


NO_CONTEST_SUPPORT = "Не поддерживаемый контест"
ARRAY_SEPARATOR = ", "


class DataManager:
	programmDirectory = ".csti"
	contestDirectory =   f"{programmDirectory}/contest"
	contestIdPath =		 f"{contestDirectory}/id"
	contestTasksIdPath = f"{contestDirectory}/tasksId"


	@staticmethod
	def saveContest(contest: Contest):
		DataManager.saveContest1(contest.id, contest.getTasksId())

	# TODO: Сделать нормальный overide функции.
	@staticmethod
	def saveContest1(id: str, tasksId: list[str]):
		os.makedirs(os.path.dirname(DataManager.contestIdPath), exist_ok=True)
		os.makedirs(os.path.dirname(DataManager.contestTasksIdPath), exist_ok=True)
	
		with open(DataManager.contestIdPath, "w") as file:
			file.write(id)
		with open(DataManager.contestTasksIdPath, "w") as file:
			file.write(ARRAY_SEPARATOR.join(tasksId))
		
	
	@staticmethod
	def loadContest():
		with open(DataManager.contestIdPath, "r") as file:
			id = file.read()
		with open(DataManager.contestTasksIdPath, "r") as file:
			tasksId = file.read().split(ARRAY_SEPARATOR)
		print(id, list(tasksId))
		contest = Contest(id, list(tasksId))
		return contest


@click.group()
def cli():
	pass


@click.command("select-contest")
@click.argument("id", type=int, required=False)
def selectContest(id: int|None):
	homework = None
	homeworksCount = ContestInterface().getAviableHomeworkCount()
	if isinstance(id, int) and id in range(1, homeworksCount):
		homework = ContestInterface().getHomework(namePattern, id)
		if homework[0] == -1:
			print("Warning: Выбран не допустимый контест.")
			return

	else:
		homeworks = list()
		lastElementIndex = 0
		for index in range(1, homeworksCount + 1):
			homework = ContestInterface().getHomework(namePattern, index)
			
			# NOTE: Заглушка, убирает не работающий пока что status.
			homeworkAdapter = (homework[0], list())
			for i in range(0, len(homework[1])):
				homeworkAdapter[1].append(homework[1][i][0]) 
			homework = homeworkAdapter
			
			if homework[0] == "-1":
				homeworks.append(NO_CONTEST_SUPPORT)
				continue
			
			homeworks.append(homework)
			lastElementIndex = len(homeworks)

		homework = inquirer.rawlist(
			message="Контест:",
			choices=homeworks,
			default=lastElementIndex,
			validate=lambda result: result != NO_CONTEST_SUPPORT,
			invalid_message="Не поддерживается!",
			vi_mode=True,
		).execute()
	
	DataManager.saveContest1(homework[0], homework[1])





cli.add_command(selectContest)
