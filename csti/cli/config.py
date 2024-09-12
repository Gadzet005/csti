from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from csti.cli.cli import cli
from csti.cli.print import cprint
from csti.config import GlobalConfig
from csti.etc.locale import Locale


@cli.group("config", help="Настройка приложения.")
def config():
    pass


@config.command("init", help="Создать шаблонный конфиг.")
def init():
    GlobalConfig()
    cprint.success("Конфиг успешно инициализирован.")


@config.command("setup", help="Изменить конфиг.")
def setup():
    config = GlobalConfig()

    cprint.info("Чтобы пропустить изменение поля нажмите enter.")
    login = inquirer.text("Логин: ", default=config.login).execute()
    config.login = login

    password = inquirer.secret(
        "Пароль: ", transformer=lambda res: "*" * len(res or config.password)
    ).execute()
    if password:
        config.password = password

    name = inquirer.text("Фамилия: ", default=config.name).execute().capitalize()
    config.name = name

    homeUrl = inquirer.text("URL домашней страницы: ", default=config.homeUrl).execute()
    config.homeUrl = homeUrl

    localeName = inquirer.select(
        "Выберите язык:",
        choices=list(map(lambda x: x.name, Locale)),
        default=config.locale.name,
        vi_mode=True,
    ).execute()
    config.locale = Locale[localeName]

    featureChoices = [
        Choice("enable-auto-tests", "Включить авто тесты", config.enableAutoTests),
        Choice(
            "enable-auto-formatting",
            "Включить авто форматирование",
            config.enableAutoFormatting,
        ),
    ]
    enabledFeatures = inquirer.checkbox(
        message="Настройка функций.", choices=featureChoices, vi_mode=True
    ).execute()

    features = config.get("features")
    for name, _ in features.items():
        features[name] = name in enabledFeatures
    config.set("features", features)

    config.save()
    cprint.success("Настройка успешно завершена.")
