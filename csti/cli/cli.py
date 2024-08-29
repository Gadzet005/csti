import click
from InquirerPy import inquirer

from csti.cli.data_manager import DataManager
from csti.cli.print import cprint, ncprint
from csti.config import ConfigManager
from csti.consts import CliConsts, Language
from csti.contest import ContestInterface, SolutionStatus
from csti.program import CompileError, Program, formatProgram, prepareProgram
from csti.program.test_result import TestStatus, TestResultList


@click.group()
def cli():
	pass


@cli.command("init", help="Инициализировать папку для работы с контестом.")
def init():
	DataManager.init()
	cprint.success("Инициализация завершена.")


@cli.command("configure", help="Настроить глобальный конфиг csti.")
def configure():
	login = inquirer.text("Введите логин: ").execute()
	password = inquirer.secret("Введите пароль: ").execute()
	name = inquirer.text("Введите фамилию: ").execute().capitalize()
	homeUrl = inquirer.text("Введите URL домашней страницы: ").execute()

	cprint.success("Настройка успешно закончена")

@cli.command("select-contest", help="Выбрать контест.")
@click.argument("local-id", type=int, required=False)
def selectContest(local_id: int|None = None):
	homework = None
	homeworsLocalId = ContestInterface().getAvailableHomeworksLocalId()
	if isinstance(local_id, int) and local_id in homeworsLocalId:
		homework = ContestInterface().getHomework(ConfigManager().name, local_id)
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


@cli.command("select-task", help="Выбрать задачу.")
@click.argument("local-id", type=int, required=False)
def selectTask(local_id: int|None = None):
	contest = DataManager.loadContest()
	taskLocalId = None
	tasksCount = len(contest.tasks)
	if isinstance(local_id, int) and local_id in range(1, tasksCount + 1):
		taskLocalId = str(local_id)

	else: 
		if local_id:
			cprint.warning("Warning: Задача отсутствует. Выберите из списка.")

		tasks = contest.tasks
		tasksName = list(map(lambda task: task.name, tasks))

		lastSucsess = 0
		for task in tasks:
			if task.solution and task.solution.status != SolutionStatus.accepted_for_review:
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


@cli.command("get-task", help="Показать информацию о выбранной задаче.")
@click.option(
	"-n", "--name", is_flag=True, default = False, 
	help="Показать название задачи."
)
@click.option(
	"-c", "--cond", is_flag=True, default = False, 
	help="Показать условие задачи."
)
@click.option(
	"-i", "--info", is_flag=True, default = False, 
	help="Показать вспомогательную информацию."
)
@click.option(
	"-t", "--tests", is_flag=True, default = False,
	help="Показать базовые тесты."
)
@click.option(
	"-s", "--solution", is_flag=True, default = False,
	help="Показать последнее отправленное решение."
)
def getTask(
	name: bool, info: bool, cond: bool, tests: bool,
	solution: bool
):
	contest = DataManager.loadContest()
	task = contest.currentTask

	flags = [name, info, cond, tests, solution]
	shouldPrintAll = not any(flags) or all(flags)
	taskPrint = cprint if shouldPrintAll else ncprint

	if name or shouldPrintAll:
		taskPrint.primary(task.name, end="\n\n")

	if info or shouldPrintAll:
		for key, value in task.info.items():
			taskPrint.info(f"{key}: {value}")
		taskPrint()

	if cond or shouldPrintAll:
		taskPrint(task.condition, end="\n\n")

	if tests or shouldPrintAll:
		for input, output in task.tests:
			taskPrint.info(f"Входные данные:")
			taskPrint(input)
			taskPrint.info(f"Результат:")
			taskPrint(output)
			taskPrint()

	if (solution or shouldPrintAll) and task.solution:
		taskPrint.primary("Последнее отправленное решение:")
		taskPrint.byFlag(
			f"{task.solution.status.value}. Тестов пройдено: {task.solution.testsPassed}",
			flag=task.solution.status == SolutionStatus.accepted_for_review
		)


def printTestResults(testResults: TestResultList):
	""" Выводит результаты тестирования программы """

	cprint.byFlag(
		f"Пройдено тестов: {testResults.passed} из {testResults.total}.", 
		flag=testResults.arePassedAll
	)

	for idx, testResult in enumerate(testResults, 1):
		cprint.byFlag(
			f"[{idx}/{testResults.total}] {testResult.status.value}",
			flag=testResult.status == TestStatus.ok
		)

		match testResult.status:
			case TestStatus.wrongAnswer:
				cprint.info("Входные данные:")
				cprint.text(testResult.input)
				cprint.info("Вывод:")
				cprint.text(testResult.output)
				cprint.info("Ожидаемый результат:")
				cprint.text(testResult.expected)
			case TestStatus.runtimeError:
				cprint.info("Входные данные:")
				cprint.text(testResult.input)
				cprint.info("Ошибка:")
				cprint.text(testResult.message)
			case TestStatus.timeLimit:
				cprint.info("Входные данные:")
				cprint.text(testResult.input)
				cprint.error("Превышено время выполнения.")
			case TestStatus.memoryLimit:
				cprint.info("Входные данные:")
				cprint.text(testResult.input)
				cprint.error("Превышено лимит памяти.")
			case _:
				pass


@cli.command("send-task", help="Отправить задачу на проверку.")
@click.argument("file", type=click.Path(exists=True), required=True)
@click.option(
	"-l", "--lang", type=str, default="auto", show_default="Автоматический",
	help="Язык программирования."
)
@click.option(
	"-t", "--no-tests", is_flag=True, default=False, 
	help="Отключает выполнение тестов."
)
@click.option(
	"-f", "--no-format", is_flag=True, default=False, 
	help="Отключает форматирование файла."
)
@click.option(
	"-c", "--no-confirm", is_flag=True, default=False, 
	help="Отключает подтверждение отправки решения."
)
def sendTask(
	file: str,
	lang: str,
	no_tests: bool,
	no_format: bool,
	no_confirm: bool
):
	contest = DataManager.loadContest()

	contestLang = contest.lang
	if lang != "auto":
		contestLang = Language.fromName(lang)
	if contestLang is None:
		cprint.warning(f"Неизвестный язык программирования: {lang}.")
		return

	program = Program(contestLang, file)

	# Тестирование
	if not no_tests:
		allTestsPassed = True
		try:
			cprint.primary("Запуск тестов...")
			with prepareProgram(program):
				testResults = program.test(
					contest.currentTask.tests,
					contest.currentTask.timeLimit,
					contest.currentTask.memoryLimit
				)
				allTestsPassed = testResults.arePassedAll
				printTestResults(testResults)
		except CompileError as error:
			cprint.error(f"Ошибка компиляции файла '{file}':")
			cprint(error)
			allTestsPassed = False

		if not allTestsPassed:
			cprint.primary("Решение не было отправлено.")
			return

	# Подтверждение отправки решения
	shouldSendSolution = True
	if not no_confirm:
		shouldSendSolution = inquirer.confirm(
			"Вы уверены что хотите отправить решение на проверку? "
			f"Оставшееся количество попыток: {contest.currentTask.remainingAttemps}.\n",
			default=False,
		).execute()

	if shouldSendSolution:
		# Форматирование кода
		if no_format or not program.canBeFormatted:
			contest.currentTask.sendSolution(program.code)
		else:
			cprint.primary("Форматирование кода...")
			with formatProgram(program) as formatted:
				contest.currentTask.sendSolution(formatted.code)
		cprint.success("Решение успешно отправлено.")
	else:
		cprint.primary("Решение не было отправлено.")
