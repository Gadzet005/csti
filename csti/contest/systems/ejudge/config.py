import typing as t

from InquirerPy import inquirer

from csti.storage import StorageTemplate
from csti.storage.config import YAMLConfig
from csti.storage.config.field import StringField
from csti.storage.config.tuner import ConfigTuner


class EjudgeConfig(YAMLConfig):
    template = StorageTemplate(
        [
            StringField("login"), 
            StringField("password"),
            StringField("url"),
        ]
    )


class EjudgeConfigTuner(ConfigTuner):
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

        homeUrl = self.config.get("home-url", default="")
        homeUrl = inquirer.text(  # type: ignore
            "URL системы: ", default=homeUrl, validate=lambda x: x
        ).execute()
        self.config["home-url"] = homeUrl
