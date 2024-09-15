import os
import typing as t

import click
from InquirerPy import inquirer

from csti.cli.state import CLIState
from csti.cli.utils.print import Printer
from csti.cli.utils.print_test_results import printTestResults
from csti.etc.language import GeneralLanguage, Language
from csti.program_view import CompileError, ProgramView, format, prepareForRun


@click.group("task", help="Взаимодействие с задачами.")
def task():
    pass


@task.command("select", help="Выбрать задачу.")
@click.argument("id", type=int, required=False)
@click.pass_obj
def selectTask(state: CLIState, id: t.Optional[int] = None):
    contest = state.env.storage.loadContest(state.manager)
    task = contest.getTask(id) if id is not None else None

    if task is None or not task.isValid:
        if task is not None:
            state.print.warning("Задача отсутствует. Выберите из списка.")

        tasks = contest.getTasks()
        taskNames = list(map(lambda task: task.name, tasks))

        taskIdx = inquirer.rawlist(  # type: ignore
            message="Задача: ",
            choices=taskNames,
            vi_mode=True,
            filter=lambda x: taskNames.index(x),
        ).execute()

        task = tasks[taskIdx]

    currentTaskId = state.env.storage.get("contest", "currentTaskId", default=None)
    if currentTaskId is not None and currentTaskId == task.id:
        state.print.warning("Эта задача уже выбрана.")
        return

    state.env.createTaskFiles([task], update=True)
    state.env.storage.set("contest", "currentTaskId", value=task.id)
    state.print.success(f"Задача успешно выбрана: {task.name}.")


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
@click.pass_obj
def showInfo(
    state: CLIState, name: bool, info: bool, cond: bool, tests: bool, solution: bool
):
    task = state.env.storage.loadCurrentTask(state.manager)

    flags = [name, info, cond, tests, solution]
    shouldPrintAll = not any(flags) or all(flags)
    taskPrint = state.print if shouldPrintAll else Printer(False)

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
        for taskSolution in task.solutions:
            taskPrint.info(f"ID: {taskSolution["id"]}")
            taskPrint.info(f"Статус: {taskSolution["status"]}")
            taskPrint.info(f"Тестов пройдено: {taskSolution["testsPassed"]}")
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
    state: CLIState,
    file: t.Optional[str],
    lang: str,
    no_tests: bool,
    no_format: bool,
    no_confirm: bool,
):
    task = state.env.storage.loadCurrentTask(state.manager)

    if file is None:
        file = state.env.getTaskFile(task)
        path = os.path.join(state.env.dir, file)
        if os.path.exists(path):
            state.print.info(f"Файл для отправки: '{file}'.")
        else:
            state.print.warning(f"Файл по пути '{path}' не найден.")
            return

    if not no_tests:
        no_tests = not state.config.get("features", "enable-auto-tests")
    if not no_format:
        no_format = not state.config.get("features", "enable-auto-formatting")

    if lang != "auto":
        selected = GeneralLanguage.fromName(lang)
        if selected is None:
            state.print.warning(f"Неизвестный язык программирования: {lang}.")
            return
        taskLang: Language = selected
    else:
        taskLang = task.language

    program = ProgramView(file, taskLang)

    # Тестирование
    if not no_tests:
        allTestsPassed = True
        try:
            state.print.primary("Запуск тестов...")
            with prepareForRun(program):
                testResults = program.test(
                    task.inputExample,
                    task.timeLimit,
                    task.memoryLimit,
                )
                allTestsPassed = testResults.arePassedAll
                printTestResults(testResults, state.print)
        except CompileError as error:
            state.print.error(f"Ошибка компиляции файла '{file}':")
            state.print(error)
            allTestsPassed = False

        if not allTestsPassed:
            state.print.primary("Решение не было отправлено.")
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
            state.print.primary("Форматирование кода...")
            with format(program, program.lang.availableformatStyles[0]) as formatted:
                task.sendSolution(formatted)
        state.print.success("Решение успешно отправлено.")
    else:
        state.print.primary("Решение не было отправлено.")
