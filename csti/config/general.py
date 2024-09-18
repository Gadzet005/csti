import os
import shutil
import typing as t

from platformdirs import user_config_dir

from csti.data_storage import Group, StorageTemplate
from csti.data_storage.config import YAMLConfig
from csti.data_storage.config.field import BoolField, EnumField, StringField
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
            EnumField("locale", enumType=Locale, default=Locale.russian),
            Group(
                "features",
                [
                    BoolField("enable-auto-tests", default=True),
                    BoolField("enable-auto-formatting", default=True),
                ],
            ),
            BoolField("debug", default=False),
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
