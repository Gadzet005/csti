import click
from InquirerPy import inquirer

from csti.cli.cli import cli
from csti.cli.data_manager import DataManager
from csti.cli.print import cprint
from csti.config import GlobalConfig
from csti.consts import CliConsts
from csti.contest import ContestInterface


@cli.group("contest", help="Работа с контестом.")
def contest():
    pass


@contest.command("init", help="Инициализировать папку для работы с контестом.")
def init():
	DataManager.init()
	cprint.success("Инициализация завершена.")


@contest.command("select", help="Выбрать контест.")
@click.argument("local-id", type=int, required=False)
def select(local_id: int|None = None):
	homework = None
	homeworsLocalId = ContestInterface().getAvailableHomeworksLocalId()
	if isinstance(local_id, int) and local_id in homeworsLocalId:
		homework = ContestInterface().getHomework(GlobalConfig().name, local_id)
		if homework[0] == "-1":
			cprint.warning("Warning: Выбран не допустимый контест.")
			return

		# NOTE: Заглушка, убирает не работающий пока что status.
		homeworkAdapter = (homework[0], list())
		for i in range(0, len(homework[1])):
			homeworkAdapter[1].append(homework[1][i][0]) 
		homework = homeworkAdapter

	else:
		if local_id != None:
			cprint.warning("Warning: Контест отсутствует. Выберите из списка.")

		homeworks = list()
		lastElementIndex = 0
		for index in homeworsLocalId:
			homework = ContestInterface().getHomework(GlobalConfig().name, index)
			
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
