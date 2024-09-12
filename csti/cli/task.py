import os

import click
from InquirerPy import inquirer

from csti.cli.cli import cli
from csti.cli.print import cprint, ncprint
from csti.cli.utils import printTestResults
from csti.config import GlobalConfig
from csti.contest import SolutionStatus
from csti.contest_env import ContestEnv
from csti.etc.language import Language
from csti.program_view import CompileError, ProgramView, format, prepareForRun


@cli.group("task", help="Взаимодействие с задачами.")
def task():
    pass


@task.command("select", help="Выбрать задачу.")
@click.argument("id", type=int, required=False)
def selectTask(id: int | None = None):
    env = ContestEnv.inCurrentDir()
    contest = env.storage.loadContest()
    task = contest.getTask(id) if id is not None else None

    if task is None or not task.isValid:
        if task is not None:
            cprint.warning("Задача отсутствует. Выберите из списка.")

        tasks = contest.getTasks()
        taskNames = list(map(lambda task: task.name, tasks))

        taskIdx = inquirer.rawlist(
            message="Задача: ",
            choices=taskNames,
            vi_mode=True,
            filter=lambda x: taskNames.index(x),
        ).execute()

        task = tasks[taskIdx]

    currentTaskId = env.storage.get("contest", "currentTaskId", default=None)
    if currentTaskId is not None and currentTaskId == task.id:
        cprint.warning("Эта задача уже выбрана.")
        return

    env.createTaskFiles([task], update=True)
    env.storage.set("contest", "currentTaskId", value=task.id)
    cprint.success(f"Задача успешно выбрана: {task.name}.")


@task.command("info", help="Показать информацию о выбранной задаче.")
@click.option(
    "-n", "--name", is_flag=True, default=False, help="Показать название задачи."
)
@click.option(
    "-c", "--cond", is_flag=True, default=False, help="Показать условие задачи."
)
@click.option(
    "-i",
    "--info",
    is_flag=True,
    default=False,
    help="Показать вспомогательную информацию.",
)
@click.option(
    "-t", "--tests", is_flag=True, default=False, help="Показать примеры тестов."
)
@click.option(
    "-s",
    "--solution",
    is_flag=True,
    default=False,
    help="Показать последнее отправленное решение.",
)
def showInfo(name: bool, info: bool, cond: bool, tests: bool, solution: bool):
    env = ContestEnv.inCurrentDir()
    task = env.storage.loadCurrentTask()

    flags = [name, info, cond, tests, solution]
    shouldPrintAll = not any(flags) or all(flags)
    taskPrint = cprint if shouldPrintAll else ncprint

    if name or shouldPrintAll:
        taskPrint.primary(task.name, end="\n\n")

    if info or shouldPrintAll:
        taskPrint.info(f"Ограничение по времени: {task.timeLimit} c")
        taskPrint.info(f"Ограничение по памяти: {task.memoryLimit} MB")
        taskPrint.info(f"Осталось посылок: {task.remainingAttempts}")
        taskPrint()

    if cond or shouldPrintAll:
        taskPrint(task.description, end="\n\n")

    if tests or shouldPrintAll:
        for input, output in task.inputExample:
            taskPrint.info(f"Входные данные:")
            taskPrint(input)
            taskPrint.info(f"Результат:")
            taskPrint(output)
            taskPrint()

    if len(task.solutions) != 0:
        taskPrint.primary("Отправленные решения:")
        for solution in task.solutions:
            taskPrint.info(f"ID: {solution["id"]}")
            taskPrint.info(f"Статус: {solution["status"]}")
            taskPrint.info(f"Тестов пройдено: {solution["testsPassed"]}")
            taskPrint()


@task.command("send", help="Отправить задачу на проверку.")
@click.argument("file", type=click.Path(exists=True), required=False)
@click.option(
    "-l",
    "--lang",
    type=str,
    default="auto",
    show_default="Автоматический выбор языка",
    help=(
        f"Язык программирования. Возможные варианты: "
        f"{list(map(lambda x: x.name, Language))}"
    ),
)
@click.option(
    "-t", "--no-tests", is_flag=True, default=False, help="Отключает выполнение тестов."
)
@click.option(
    "-f",
    "--no-format",
    is_flag=True,
    default=False,
    help="Отключает форматирование файла.",
)
@click.option(
    "-c",
    "--no-confirm",
    is_flag=True,
    default=False,
    help="Отключает подтверждение отправки решения.",
)
def sendTask(
    file: str | None, lang: str, no_tests: bool, no_format: bool, no_confirm: bool
):
    env = ContestEnv.inCurrentDir()
    task = env.storage.loadCurrentTask()
    config = GlobalConfig()

    if file is None:
        file = env.getTaskFile(task)
        path = os.path.join(env.dir, file)
        if os.path.exists(path):
            cprint.info(f"Файл для отправки: '{file}'.")
        else:
            cprint.warning(f"Файл по пути '{path}' не найден.")
            return

    if not no_tests:
        no_tests = not config.enableAutoTests
    if not no_format:
        no_format = not config.enableAutoFormatting

    taskLang = task.language
    if lang != "auto":
        taskLang = Language.fromName(lang)
    if taskLang is None:
        cprint.warning(f"Неизвестный язык программирования: {lang}.")
        return

    program = ProgramView(file, taskLang)

    # Тестирование
    if not no_tests:
        allTestsPassed = True
        try:
            cprint.primary("Запуск тестов...")
            with prepareForRun(program):
                testResults = program.test(
                    task.inputExample,
                    task.timeLimit,
                    task.memoryLimit,
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
            f"Оставшееся количество попыток: {task.remainingAttempts}.\n",
            default=False,
        ).execute()

    if shouldSendSolution:
        # Форматирование кода
        if no_format or len(program.lang.availableformatStyles) == 0:
            task.sendSolution(program)
        else:
            cprint.primary("Форматирование кода...")
            with format(program, program.lang.availableformatStyles[0]) as formatted:
                task.sendSolution(formatted)
        cprint.success("Решение успешно отправлено.")
    else:
        cprint.primary("Решение не было отправлено.")
