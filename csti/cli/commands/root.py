import typing as t

import click

from csti.cli.commands.config import config
from csti.cli.commands.contest import contest
from csti.cli.commands.task import task
from csti.cli.state import CLIState
from csti.etc.consts import APP_NAME, APP_VERSION

CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
}


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(APP_VERSION, "-v", "--version", package_name=APP_NAME)
def root():
    """CSTI - Contest System Terminal Interface."""
    pass


root.add_command(contest)
root.add_command(config)
root.add_command(task)


@root.command("init")
@click.argument("dir", type=click.Path(exists=True), required=False)
@click.pass_obj
def init(state: CLIState, dir: t.Optional[str]):
    """Инициализировать папку для работы с контестом."""

    state.env.create(dir)
    state.print.success("Инициализация завершена.")
