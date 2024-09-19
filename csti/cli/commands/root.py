import typing as t

import click
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from csti.cli.commands.contest import contest
from csti.cli.commands.task import task
from csti.cli.state import CLIState
from csti.etc.consts import APP_NAME, APP_VERSION
from csti.etc.locale import Locale

CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
}


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(APP_VERSION, "-v", "--version", package_name=APP_NAME)
def root():
    """CSTI - Contest System Terminal Interface."""
    pass


root.add_command(contest)
root.add_command(task)


@root.command("init")
@click.argument("dir", type=click.Path(exists=True), required=False)
@click.pass_obj
def init(state: CLIState, dir: t.Optional[str]):
    """Инициализировать папку для работы с контестом."""

    state.createEnv(dir)
    state.print.success("Инициализация завершена.")


@root.command("configure")
@click.pass_obj
def configure(state: CLIState):
    """Настроить конфиг."""

    config = state.config

    state.print.info("Чтобы пропустить изменение поля нажмите enter.")
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
    state.print.success("Настройка успешно завершена.")
