import typing as t

from InquirerPy import inquirer

from csti.contest.systems.contest_solutions.locale import Locale
from csti.storage import Group, StorageTemplate
from csti.storage.config import YAMLConfig
from csti.storage.config.field import EnumField, StringField
from csti.storage.config.tuner import ConfigTuner


class ContestSolutionsConfig(YAMLConfig):
    template = StorageTemplate(
        [
            Group(
                "user",
                [StringField("login"), StringField("password"), StringField("name")],
            ),
            StringField("home-url"),
            EnumField("locale", enumType=Locale, default=Locale.russian),
        ]
    )


class ContestSolutionsConfigTuner(ConfigTuner):
    @t.override
    def _tune(self):
        login = self.config.get("user", "login", default="")
        login = inquirer.text(  # type: ignore
            "Логин: ", default=login, validate=lambda x: x
        ).execute()
        self.config["user", "login"] = login

        currentPassword = self.config.get("user", "password", default="")
        password = inquirer.secret(  # type: ignore
            "Пароль: ",
            transformer=lambda res: "*" * len(res or currentPassword),
            validate=lambda res: res or currentPassword,
        ).execute()
        if password:
            self.config["user", "password"] = password

        name = self.config.get("user", "name", default="")
        name = (
            inquirer.text("Фамилия: ", default=name, validate=lambda x: x)  # type: ignore
            .execute()
            .capitalize()
        )
        self.config["user", "name"] = name

        homeUrl = self.config.get("home-url", default="")
        homeUrl = inquirer.text(  # type: ignore
            "URL домашней страницы: ", default=homeUrl, validate=lambda x: x
        ).execute()
        self.config["home-url"] = homeUrl

        locale = self.config.get("locale", default=Locale.russian)
        locale = inquirer.select(  # type: ignore
            "Выберите язык:",
            choices=[locale.name for locale in Locale],
            default=locale.name,
            filter=lambda loc: Locale[loc],
            vi_mode=True,
        ).execute()
        self.config["locale"] = locale
