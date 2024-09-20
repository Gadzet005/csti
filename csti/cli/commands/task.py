import os
import typing as t

import click
from InquirerPy import inquirer

from csti.cli.cli import ContestCLI
from csti.cli.utils.print import Printer
from csti.cli.utils.print_test_results import printTestResults
from csti.etc.language import GeneralLanguage, Language
from csti.program_view import CompileError, ProgramView, format, prepareForRun


@click.group("task")
def task():
    """Работа с задачами."""
    pass


@task.command("select")
@click.argument("id", type=int, required=False)
@click.pass_obj
def selectTask(cli: ContestCLI, id: t.Optional[int] = None):
    """Выбрать задачу."""

    env = cli.getEnv()
    contest = env.storage.loadContest(cli.manager)
    task = contest.getTask(id) if id is not None else None

    if task is None or not task.isValid:
        if task is not None:
            cli.print.warning("Задача отсутствует. Выберите из списка.")

        tasks = contest.getTasks()
        taskNames = list(map(lambda task: task.name, tasks))

        taskIdx = inquirer.rawlist(  # type: ignore
            message="Задача: ",
            choices=taskNames,
            vi_mode=True,
            filter=lambda x: taskNames.index(x),
        ).execute()

        task = tasks[taskIdx]

    currentTaskId = env.storage.get("contest", "currentTaskId", default=None)
    if currentTaskId is not None and currentTaskId == task.id:
        cli.print.warning("Эта задача уже выбрана.")
        return

    env.createTaskFiles([task], update=True)
    env.storage.set("contest", "currentTaskId", value=task.id)
    cli.print.success(f"Задача успешно выбрана: {task.name}.")


@task.command("info")
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
@click.pass_obj
def showInfo(
    cli: ContestCLI, name: bool, info: bool, cond: bool, tests: bool, solution: bool
):
    """Показать информацию о выбранной задаче."""

    env = cli.getEnv()
    task = env.storage.loadCurrentTask(cli.manager)

    flags = [name, info, cond, tests, solution]
    shouldPrintAll = not any(flags) or all(flags)

    taskPrint = cli.print if shouldPrintAll else Printer(cli.print.file, True)

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

    if len(task.solutions) != 0 and (solution or shouldPrintAll):
        taskPrint.primary("Отправленные решения:")
        for taskSolution in task.solutions:
            taskPrint.info(f"ID: {taskSolution["id"]}")
            taskPrint.info(f"Статус: {taskSolution["status"]}")
            taskPrint.info(f"Тестов пройдено: {taskSolution["testsPassed"]}")
            taskPrint()


@task.command("send")
@click.argument("file", type=click.Path(exists=True), required=False)
@click.option(
    "-l",
    "--lang",
    type=str,
    default="auto",
    show_default="Автоматический выбор языка",
    help=(
        f"Язык программирования. Возможные варианты: "
        f"{list(map(lambda x: x.name, GeneralLanguage))}"
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
@click.pass_obj
def sendTask(
    cli: ContestCLI,
    file: t.Optional[str],
    lang: str,
    no_tests: bool,
    no_format: bool,
    no_confirm: bool,
):
    """Отправить задачу на проверку."""

    env = cli.getEnv()
    task = env.storage.loadCurrentTask(cli.manager)

    if file is None:
        file = env.getTaskFile(task)
        path = os.path.join(env.dir, file)
        if os.path.exists(path):
            cli.print.info(f"Файл для отправки: '{file}'.")
        else:
            cli.print.warning(f"Файл по пути '{path}' не найден.")
            return

    if not no_tests:
        no_tests = not cli.config.get("features", "enable-auto-tests")
    if not no_format:
        no_format = not cli.config.get("features", "enable-auto-formatting")

    if lang != "auto":
        selected = GeneralLanguage.fromName(lang)
        if selected is None:
            cli.print.warning(f"Неизвестный язык программирования: {lang}.")
            return
        taskLang: Language = selected
    else:
        taskLang = task.language

    program = ProgramView(file, taskLang)

    # Тестирование
    if not no_tests:
        allTestsPassed = True
        try:
            cli.print.primary("Запуск тестов...")
            with prepareForRun(program):
                testResults = program.test(
                    task.inputExample,
                    task.timeLimit,
                    task.memoryLimit,
                )
                allTestsPassed = testResults.arePassedAll
                printTestResults(testResults, cli.print)
        except CompileError as error:
            cli.print.error(f"Ошибка компиляции файла '{file}':")
            cli.print(error)
            allTestsPassed = False

        if not allTestsPassed:
            cli.print.primary("Решение не было отправлено.")
            return

    # Подтверждение отправки решения
    shouldSendSolution = True
    if not no_confirm:
        shouldSendSolution = inquirer.confirm(  # type: ignore
            "Вы уверены что хотите отправить решение на проверку? "
            f"Оставшееся количество попыток: {task.remainingAttempts}.\n",
            default=False,
        ).execute()

    if shouldSendSolution:
        # Форматирование кода
        if no_format or len(program.lang.availableformatStyles) == 0:
            task.sendSolution(program)
        else:
            cli.print.primary("Форматирование кода...")
            with format(program, program.lang.availableformatStyles[0]) as formatted:
                task.sendSolution(formatted)
        cli.print.success("Решение успешно отправлено.")
    else:
        cli.print.primary("Решение не было отправлено.")
