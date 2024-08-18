import click
from InquirerPy import inquirer

from cli.data_manager import DataManager
from config import ConfigManager
from consts import CliConsts
from contest.contest_interface import ContestInterface
from contest.task.solution import SolutionStatus


@click.group()
def cli():
	pass


@cli.command("init")
def init():
	DataManager.init()


@cli.command("select-contest")
@click.argument("local-id", type=int, required=False)
def selectContest(local_id: int|None = None):
	homework = None
	homeworksCount = ContestInterface().getAviableHomeworkCount()
	if isinstance(local_id, int) and local_id in range(1 + 6, homeworksCount + 1 + 6):
		homework = ContestInterface().getHomework(ConfigManager().name, local_id)
		if homework[0] == "-1":
			print("Warning: Выбран не допустимый контест.")
			return

		# NOTE: Заглушка, убирает не работающий пока что status.
		homeworkAdapter = (homework[0], list())
		for i in range(0, len(homework[1])):
			homeworkAdapter[1].append(homework[1][i][0]) 
		homework = homeworkAdapter

	else:
		if local_id != None:
			print("Warning: Контест отсутствует. Выберите из списка.")

		homeworks = list()
		lastElementIndex = 0
		for index in range(1 + 6, homeworksCount + 1 + 6):
			homework = ContestInterface().getHomework(ConfigManager().name, index)
			
			# NOTE: Заглушка, убирает не работающий пока что status.
			homeworkAdapter = (homework[0], list())
			for i in range(0, len(homework[1])):
				homeworkAdapter[1].append(homework[1][i][0]) 
			homework = homeworkAdapter
			
			if homework[0] == "-1":
				homeworks.append(CliConsts.NO_CONTEST_SUPPORT)
				continue
			
			homeworks.append(homework)
			lastElementIndex = len(homeworks)

		homework = inquirer.rawlist(
			message = "Контест:",
			choices = homeworks,
			default = lastElementIndex,
			validate = lambda result: result != CliConsts.NO_CONTEST_SUPPORT,
			invalid_message = "Не поддерживается!",
			vi_mode = True,
		).execute()
	
	DataManager.saveContest(homework[0], homework[1])



@cli.command("select-task")
@click.argument("local-id", type=int, required=False)
def selectTask(local_id: int|None = None):
	contest = DataManager.loadContest()
	taskLocalId = None
	tasksCount = len(contest.tasks)
	if isinstance(local_id, int) and local_id in range(1, tasksCount + 1):
		taskLocalId = str(local_id)

	else: 
		if local_id != None:
			print("Warning: Задача отсутствует. Выберите из списка.")

		tasks = contest.tasks
		tasksName = list(map(lambda task: task.getName(), tasks))

		lastSucsess = 0
		for task in tasks:
			solution = task.getSolution()
			if solution and solution.status != SolutionStatus.accepted_for_review:
				break
			lastSucsess += 1
		
		task = inquirer.rawlist(
			message = "Задача: ",
			choices = tasksName,
			default = (lastSucsess + 1) % tasksCount,
			vi_mode = True,
			
		).execute()

		taskLocalId = str(tasksName.index(task) + 1)
	DataManager.saveContest(taskLocalId=taskLocalId)



@cli.command("task")
@click.option("--name", is_flag=True, default = False)
@click.option("--cond", is_flag=True, default = False)
@click.option("--info", is_flag=True, default = False)
@click.option("--tests", is_flag=True, default = False)
@click.option("--solution", is_flag=True, default = False)
def taskInterface(name: bool, info: bool, cond: bool, tests: bool, \
				  solution: bool):
	contest = DataManager.loadContest()
	task = contest.currentTask
	if name:
		print(task.getName())
	
	if info:
		print(task.getInfo())

	if cond:
		print(task.getCondition())

	if tests:
		print(task.getTests())

	if solution:
		print(task.getSolution())



@cli.command("send-task")
@click.argument("file", type=click.Path(exists=True), required=False)
def sendTask(file: str):
	with open(file, "r") as file_:
		programm = file_.read()
	contest = DataManager.loadContest()
	contest.currentTask.sendSolution(programm)

