import typing as t

from InquirerPy import inquirer

from csti.storage import StorageTemplate
from csti.storage.config import YAMLConfig
from csti.storage.config.field import StringField
from csti.storage.config.tuner import ConfigTuner


class Ejudge2KursVmkConfig(YAMLConfig):
    template = StorageTemplate(
        [
            StringField("login"), 
            StringField("password"),
            StringField("url"),
            StringField("contest-id")
        ]
    )


class Ejudge2KursVmkConfigTuner(ConfigTuner):
    @t.override
    def _tune(self):
        login = self.config.get("login", default="")
        login = inquirer.text(  # type: ignore
            "Логин: ", default=login, validate=lambda x: x
        ).execute()
        self.config["login"] = login

        currentPassword = self.config.get("password", default="")
        password = inquirer.secret(  # type: ignore
            "Пароль: ",
            transformer=lambda res: "*" * len(res or currentPassword),
            validate=lambda res: res or currentPassword,
        ).execute()
        if password:
            self.config["password"] = password

        homeUrl = self.config.get("url", default="")
        homeUrl = inquirer.text(  # type: ignore
            "URL системы: ", default=homeUrl, validate=lambda x: x
        ).execute()
        self.config["url"] = homeUrl

        contestId = self.config.get("contest-id", default="")
        contestId = inquirer.text(  # type: ignore
            "Id контеста: ", default=contestId, validate=lambda x: x
        ).execute()
        self.config["contest-id"] = contestId
