import typing as t

import click
from InquirerPy import inquirer

from csti.cli.state import CLIState


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
def select(state: CLIState, id: t.Optional[int], force: bool):
    """Выбрать контест."""

    env = state.env

    contest = None
    if id:
        contest = state.manager.getContest(id)

    if contest is None or not contest.isValid:
        if contest is not None:
            state.print.warning("Контест с таким id отсутствует. Выберите из списка.")

        contests = state.manager.getContests()
        lastElementIndex = len(contests)
        contestNames = [contest.name for contest in contests]

        contestIdx = inquirer.rawlist(  # type: ignore
            message="Контест:",
            choices=contestNames,
            default=lastElementIndex,
            vi_mode=True,
            filter=lambda x: contestNames.index(x),
        ).execute()

        contest = contests[contestIdx]

    if not force:
        currentContestId = env.storage.get("contest", "id", default=None)
        if currentContestId is not None and currentContestId == contest.id:
            state.print.warning("Этот контест уже выбран.")
            return

    env.selectContest(contest)
    state.print.success(f"Контест успешно выбран.")


@contest.command("info")
@click.pass_obj
def showInfo(state: CLIState):
    """Информация о текущем контесте."""

    contest = state.env.storage.loadContest(state.manager)

    state.print.primary(contest.name)
    for task in contest.getTasks():
        state.print.text("-", task.name)
