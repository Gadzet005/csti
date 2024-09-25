import typing as t

import click
from InquirerPy import inquirer

from csti.cli.commands.contest import contest
from csti.cli.commands.task import task
from csti.cli.cli import ContestCLI
from csti.etc.consts import APP_NAME, APP_VERSION
from csti.contest.systems import SupportedContestSystem
from csti.contest.env import ContestEnv


@click.group()
@click.version_option(APP_VERSION, "-v", "--version", package_name=APP_NAME)
def root():
    """CSTI - Contest System Terminal Interface."""
    pass


root.add_command(contest)
root.add_command(task)


@root.command("init")
@click.argument("dir", type=click.Path(), required=False)
@click.pass_obj
def init(cli: ContestCLI, dir: t.Optional[str]):
    """Инициализировать директорию для работы с контестом."""

    if ContestEnv(dir).isInitialized:
        cli.print.warning(
            "Директория уже инициализирована. Для настройки используйте csti configure."
        )
        return

    system = inquirer.select( # type: ignore
        "Выберите систему контестов:",
        choices=[system.name for system in SupportedContestSystem],
        filter=lambda system: SupportedContestSystem[system],
        vi_mode=True,
    ).execute()

    cli.createEnv(dir, system)

    cli.print.primary("Настройка конфига системы.")
    tuner = cli.getEnv().getConfigTuner()
    tuner.tune()

    cli.print.success("Окружение успешно создано.")


@root.command("configure")
@click.pass_obj
def configure(cli: ContestCLI):
    """Настроить конфиг."""

    cli.print.info("Чтобы пропустить изменение поля нажмите enter.")

    tuner = cli.getEnv().getConfigTuner()
    tuner.tune()
    
    cli.print.success("Настройка успешно завершена.")
