import typing as t

import click
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from csti.cli.commands.contest import contest
from csti.cli.commands.task import task
from csti.cli.cli import ContestCLI
from csti.etc.consts import APP_NAME, APP_VERSION
from csti.etc.locale import Locale
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

    env = cli.getEnv(dir, False)
    alreadyInitialized = env.isInitialized

    env.init()

    if alreadyInitialized:
        cli.print.success("Повторная инициализация директории.")
    else:
        cli.print.success("Директория инициализирована.")


@root.command("configure")
@click.pass_obj
def configure(cli: ContestCLI):
    """Настроить конфиг."""

    config = cli.config

    cli.print.info("Чтобы пропустить изменение поля нажмите enter.")
    login = inquirer.text(  # type: ignore
        "Логин: ", default=config["user", "login"]
    ).execute()
    config["user", "login"] = login

    currentPassword = config["user", "password"]
    password = inquirer.secret(  # type: ignore
        "Пароль: ", transformer=lambda res: "*" * len(res or currentPassword)
    ).execute()
    if password:
        config["user", "password"] = password

    name = (
        inquirer.text("Фамилия: ", default=config["user", "name"])  # type: ignore
        .execute()
        .capitalize()
    )
    config["user", "name"] = name

    homeUrl = inquirer.text(  # type: ignore
        "URL домашней страницы: ", default=config["home-url"]
    ).execute()
    config["home-url"] = homeUrl

    locale = inquirer.select(  # type: ignore
        "Выберите язык:",
        choices=[locale.name for locale in Locale],
        default=config["locale"].name,
        filter=lambda loc: Locale[loc],
        vi_mode=True,
    ).execute()
    config["locale"] = locale

    featureChoices = [
        Choice(
            "enable-auto-tests",
            "Включить авто тесты",
            config["features", "enable-auto-tests"],
        ),
        Choice(
            "enable-auto-formatting",
            "Включить авто форматирование",
            config["features", "enable-auto-formatting"],
        ),
    ]
    enabledFeatures = inquirer.checkbox(  # type: ignore
        message="Настройка функций.", choices=featureChoices, vi_mode=True
    ).execute()

    for choice in featureChoices:
        config["features", choice.value] = choice.value in enabledFeatures

    config.save()
    cli.print.success("Настройка успешно завершена.")
