import click
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from csti.cli.data_manager import DataManager
from csti.cli.print import cprint
from csti.config import GlobalConfig
from csti.consts import CliConsts, Locale
from csti.contest import ContestInterface


@click.group()
def cli():
	pass


@cli.command("init", help="Инициализировать папку для работы с контестом.")
def init():
	DataManager.init()
	cprint.success("Инициализация завершена.")


@cli.command("configure", help="Настроить глобальный конфиг csti.")
def configure():
	config = GlobalConfig()

	cprint.info("Чтобы не изменять поле нажмите enter.")
	login = inquirer.text("Логин: ", default=config.login).execute()
	config.login = login

	password = inquirer.secret("Пароль: ").execute()
	if password: config.password = password

	name = inquirer.text("Фамилия: ", default=config.name).execute().capitalize()
	config.name = name

	homeUrl = inquirer.text("URL домашней страницы: ", default=config.homeUrl).execute()
	config.homeUrl = homeUrl
	
	localeName = inquirer.select(
		"Выберите язык:",
		choices=list(map(lambda x: x.name, Locale)),
		default=config.locale.name,
	).execute()
	config.locale = Locale[localeName]

	featureChoices = [
		Choice(
			"enable-auto-tests", 
			"Включить авто тесты", 
			config.enableAutoTests
		),
		Choice(
			"enable-auto-formatting", 
			"Включить авто форматирование", 
			config.enableAutoFormatting
		)
	]
	enabledFeatures = inquirer.checkbox(
		message="Настройка функций.", choices=featureChoices
	).execute()

	features = config.get("features")
	for name, _ in features.items():
		features[name] = name in enabledFeatures
	config.set("features", features)

	config.save()
	cprint.success("Настройка успешно завершена.")


@cli.command("select-contest", help="Выбрать контест.")
@click.argument("local-id", type=int, required=False)
def selectContest(local_id: int|None = None):
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
