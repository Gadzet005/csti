import os
import shutil
import typing as t

from platformdirs import user_config_dir

from csti.config.config import YAMLConfig
from csti.data_storage import StorageTemplate, Group
from csti.config.field import StringField, EnumField, BoolField
from csti.etc.locale import Locale


class GeneralConfig(YAMLConfig):
    """Глобальный конфиг приложения."""

    TEMPLATE_CONFIG_PATH = "csti/config/template/config.yaml"

    template = StorageTemplate(
        [
            StringField("contest-system"),
            Group(
                "user",
                [StringField("login"), StringField("password"), StringField("name")],
            ),
            StringField("home-url"),
            EnumField("locale", enumType=Locale, defaultValue=Locale.russian),
            Group(
                "features",
                [
                    BoolField("enable-auto-tests", defaultValue=True),
                    BoolField("enable-auto-formatting", defaultValue=True),
                ],
            ),
            BoolField("debug", defaultValue=False),
        ]
    )

    @classmethod
    def forApp(cls, appName: str) -> t.Self:
        return cls(user_config_dir(appName) + "/config.yaml")

    @t.override
    def create(self):
        if not os.path.exists(self.path):
            os.makedirs(os.path.dirname(self.path))
            shutil.copyfile(self.TEMPLATE_CONFIG_PATH, self.path)
