import typing as t

import click

from csti.cli.commands.config import config
from csti.cli.commands.contest import contest
from csti.cli.commands.task import task
from csti.cli.state import CLIState
from csti.etc.consts import APP_NAME, APP_VERSION


@click.group(help="CSTI - Contest System Terminal Interface.")
@click.version_option(APP_VERSION, "-v", "--version", package_name=APP_NAME)
def root():
    pass


root.add_command(contest)
root.add_command(config)
root.add_command(task)


@root.command("init", help="Инициализировать папку для работы с контестом.")
@click.argument("dir", type=click.Path(exists=True), required=False)
@click.pass_obj
def init(state: CLIState, dir: t.Optional[str]):
    state.env.create(dir)
    state.print.success("Инициализация завершена.")
