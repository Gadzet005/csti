import os
import typing as t

from platformdirs import user_config_dir

from csti.storage import Group, StorageTemplate
from csti.storage.config.field import BoolField, StringField
from csti.storage.config.yaml import YAMLConfig


class GeneralConfig(YAMLConfig):
    """Глобальный конфиг приложения."""

    template = StorageTemplate(
        [
            Group(
                "features",
                [
                    BoolField("enable-auto-tests", default=False),
                    BoolField("enable-auto-formatting", default=True),
                ],
            ),
            Group(
                "directories",
                [
                    StringField("archive-dir", default=".csti/"),
                    StringField("contest-dir-template", default="contest#/"),
                    StringField("task-name-template", default="task#"),
                ],
            ),
            BoolField("use-color", default=True),
            BoolField("debug", default=False),
        ]
    )

    @classmethod
    def forApp(cls, appName: str) -> t.Self:
        path = os.path.join(user_config_dir(appName), "config.yaml")
        return cls(path)

    @t.override
    def create(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        super().create()
