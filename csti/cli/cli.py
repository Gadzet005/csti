import click

from csti.cli.print import cprint
from csti.contest_env import ContestEnv


@click.group()
def cli():
	pass


@cli.command("init", help="Инициализировать папку для работы с контестом.")
@click.argument("dir", type=click.Path(exists=True), required=False)
def init(dir: str|None):
	ContestEnv.init(dir)
	cprint.success("Инициализация завершена.")
