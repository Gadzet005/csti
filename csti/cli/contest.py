import click
from InquirerPy import inquirer

from csti.cli.cli import cli
from csti.cli.print import cprint
from csti.contest import Contest
from csti.contest_env import ContestEnv
from csti.contest_systems import getManager


@cli.group("contest", help="Работа с контестом.")
def contest():
    pass


@contest.command("select", help="Выбрать контест.")
@click.argument("id", type=int, required=False)
@click.option(
    "-f",
    "--force",
    default=False,
    is_flag=True,
    help="Выбирает контест, даже если он уже выбран (обновляет данные).",
)
def select(id: int | None, force: bool):
    env = ContestEnv.inCurrentDir()
    manager = getManager()
    contest = manager.getContest(id) if id is not None else None

    if contest is None or not contest.isValid:
        if contest is not None:
            cprint.warning("Контест с таким id отсутствует. Выберите из списка.")

        contests = manager.getContests()
        contestNames = [contest.name for contest in contests]

        contestIdx = inquirer.rawlist(
            message="Контест:",
            choices=[contest.name for contest in contests],
            vi_mode=True,
            filter=lambda x: contestNames.index(x),
        ).execute()

        contest = contests[contestIdx]

    if not force:
        currentContestId = env.storage.get("contest", "id", default=None)
        if currentContestId is not None and currentContestId == contest.id:
            cprint.warning("Этот контест уже выбран.")
            return

    env.selectContest(contest)
    cprint.success(f"Контест успешно выбран.")


@contest.command("info", help="Информация о текущем контесте.")
def showInfo():
    env = ContestEnv.inCurrentDir()
    contest = env.storage.loadContest()

    cprint.primary(contest.name)
    for task in contest.getTasks():
        cprint.text("-", task.name)
