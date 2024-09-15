import click
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from csti.cli.state import CLIState
from csti.etc.locale import Locale


@click.group("config", help="Настройка приложения.")
def config():
    pass


@config.command("setup", help="Изменить конфиг.")
@click.pass_obj
def setup(state: CLIState):
    config = state.app.config

    state.print.info("Чтобы пропустить изменение поля нажмите enter.")
    login = inquirer.text(  # type: ignore
        "Логин: ", default=config.get("user", "login")
    ).execute()
    config.set("user", "login", value=login)

    currentPassword = config.get("user", "password")
    password = inquirer.secret(  # type: ignore
        "Пароль: ", transformer=lambda res: "*" * len(res or currentPassword)
    ).execute()
    if password:
        config.set("user", "password", value=password)

    name = (
        inquirer.text("Фамилия: ", default=config.get("user", "name"))  # type: ignore
        .execute()
        .capitalize()
    )
    config.set("user", "name", value=name)

    homeUrl = inquirer.text(  # type: ignore
        "URL домашней страницы: ", default=config.get("home-url")
    ).execute()
    config.set("home-url", value=homeUrl)

    locale = inquirer.select(  # type: ignore
        "Выберите язык:",
        choices=[locale.name for locale in Locale],
        default=config.get("locale").name,
        filter=lambda loc: Locale[loc],
        vi_mode=True,
    ).execute()
    config.set("locale", value=locale)

    featureChoices = [
        Choice(
            "enable-auto-tests",
            "Включить авто тесты",
            config.get("features", "enable-auto-tests"),
        ),
        Choice(
            "enable-auto-formatting",
            "Включить авто форматирование",
            config.get("features", "enable-auto-formatting"),
        ),
    ]
    enabledFeatures = inquirer.checkbox(  # type: ignore
        message="Настройка функций.", choices=featureChoices, vi_mode=True
    ).execute()

    for choice in featureChoices:
        config.set("features", choice.value, value=choice.value in enabledFeatures)

    config.save()
    state.print.success("Настройка успешно завершена.")
