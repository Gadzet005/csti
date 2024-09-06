import os

import click
from InquirerPy import inquirer

from csti.cli.cli import cli
from csti.cli.print import cprint, ncprint
from csti.cli.utils import printTestResults
from csti.config import GlobalConfig
from csti.consts import Language
from csti.contest import SolutionStatus
from csti.contest_env import ContestEnv
from csti.program import CompileError, Program, formatProgram, prepareProgram


@cli.group("task", help="Взаимодействие с задачами.")
def task():
	pass


@task.command("select", help="Выбрать задачу.")
@click.argument("task-id", type=str, required=False)
def selectTask(task_id: str|None = None):
	env = ContestEnv.inCurrentDir()
	contest = env.storage.loadContest()
	tasks = contest.tasks

	currentTask = task_id
	if task_id is None or contest.getTask(task_id) is None:
		if task_id:
			cprint.warning("Задача отсутствует. Выберите из списка.")

		lastSucsess = 0
		for task in tasks:
			if task.solution and task.solution.status != SolutionStatus.accepted_for_review:
				break
			lastSucsess += 1
		defaultTaskIdx = (lastSucsess + 1) % len(tasks)
		
		taskNames = list(map(lambda task: task.name, tasks))
		taskName = inquirer.rawlist(
			message = "Задача: ",
			choices = taskNames,
			default = defaultTaskIdx,
			vi_mode = True,
		).execute()

		currentTask = tasks[taskNames.index(taskName)].id

	cprint.success(f"Задача успешно выбрана: {contest.getTask(currentTask).name}.")
	env.storage.set("contest", "currentTask", value=currentTask)


@task.command("get", help="Показать информацию о выбранной задаче.")
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
	help="Показать примеры тестов."
)
@click.option(
	"-s", "--solution", is_flag=True, default = False,
	help="Показать последнее отправленное решение."
)
def getTask(
	name: bool, info: bool, cond: bool, tests: bool,
	solution: bool
):	
	env = ContestEnv.inCurrentDir()
	contest = env.storage.loadContest()
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


@task.command("send", help="Отправить задачу на проверку.")
@click.argument("file", type=click.Path(exists=True), required=False)
@click.option(
	"-l", "--lang", type=str, default="auto", 
	show_default="Автоматический выбор языка",
	help=(
		f"Язык программирования. Возможные варианты: "
		f"{list(map(lambda x: x.name, Language))}"
	)
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
	file: str|None,
	lang: str,
	no_tests: bool,
	no_format: bool,
	no_confirm: bool
):
	env = ContestEnv.inCurrentDir()
	contest = env.storage.loadContest()
	config = GlobalConfig()

	if file is None:
		file = env.getTaskFilePath(contest.currentTask.id, contest.lang)
		if os.path.exists(file):
			cprint.info(f"Файл для отправки: '{os.path.basename(file)}'.")
		else:
			cprint.warning(f"Файл '{file}' не найден.")
			return


	if not no_tests:
		no_tests = not config.enableAutoTests
	if not no_format:
		no_format = not config.enableAutoFormatting

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
			contest.currentTask.sendSolution(program.code, program.lang.id)
		else:
			cprint.primary("Форматирование кода...")
			with formatProgram(program) as formatted:
				contest.currentTask.sendSolution(formatted.code, formatted.lang.id)
		cprint.success("Решение успешно отправлено.")
	else:
		cprint.primary("Решение не было отправлено.")
