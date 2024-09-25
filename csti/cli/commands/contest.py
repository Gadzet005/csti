import typing as t

import click
from InquirerPy import inquirer

from csti.cli.cli import ContestCLI


@click.group("contest")
def contest():
    """Работа с контестом."""
    pass


@contest.command("select")
@click.argument("id", type=int, required=False)
@click.option(
    "-f",
    "--force",
    default=False,
    is_flag=True,
    help="Выбирает контест, даже если он уже выбран (обновляет данные).",
)
@click.pass_obj
def select(cli: ContestCLI, id: t.Optional[int], force: bool):
    """Выбрать контест."""

    env = cli.getEnv()
    manager = env.getContestManager()

    contest = None
    if id:
        contest = manager.getContest(id)

    if contest is None or not contest.isValid:
        if contest is not None:
            cli.print.warning("Контест с таким id отсутствует. Выберите из списка.")

        contests = manager.getContests()
        contestNames = [contest.name for contest in contests]

        contestIdx = inquirer.rawlist(  # type: ignore
            message="Контест:",
            choices=contestNames,
            default=len(contestNames),
            vi_mode=True,
            filter=lambda x: contestNames.index(x),
        ).execute()

        contest = contests[contestIdx]

    if not force:
        currentContestId = env.storage.get("contest", "id", default=None)
        if currentContestId is not None and currentContestId == contest.id:
            cli.print.warning("Этот контест уже выбран.")
            return

    env.selectContest(contest)
    cli.print.success(f"Контест успешно выбран.")


@contest.command("info")
@click.pass_obj
def showInfo(cli: ContestCLI):
    """Информация о текущем контесте."""

    env = cli.getEnv()
    manager = env.getContestManager()
    contest = env.storage.loadContest(manager)

    cli.print.primary(contest.name)
    for task in contest.getTasks():
        cli.print.text("-", task.name)
