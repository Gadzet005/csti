import os
import shutil
from typing import Any

import yaml
from platformdirs import user_config_dir

from csti.config.utils import configField
from csti.etc.locale import Locale
from csti.etc.settings import APP_NAME
from csti.etc.utils import Singleton

appConfigDir = user_config_dir(APP_NAME)
globalConfigPath = f"{appConfigDir}/config.yaml"
configTemplateDir = "csti/config/config_template"


class Config(metaclass=Singleton):
    def __init__(self):
        self._data: dict = {}

        if not os.path.exists(globalConfigPath):
            self.createDefaultConfig()
        self.load()

    @staticmethod
    def createDefaultConfig():
        """Генерация конфигурационного файла из шаблона."""
        shutil.copytree(configTemplateDir, appConfigDir, dirs_exist_ok=True)

    def load(self):
        """Получение данных из конфигурационного файла."""
        with open(globalConfigPath, "r") as file:
            self._data = yaml.safe_load(file)

    def save(self):
        """Сохранение данных в конфигурационный файл."""
        with open(globalConfigPath, "w") as file:
            yaml.dump(self._data, file, allow_unicode=True, sort_keys=False)

    def _pull(self, key: str, nestedIn: list | None):
        if nestedIn is None:
            nestedIn = []

        data = self._data
        for name in nestedIn:
            data = data.get(name)
            if data is None:
                break

        if data is None or key not in data:
            field = ".".join(nestedIn + [key])
            raise KeyError(f"Поле {field} не найдено в глобальном конфиге")

        return data

    def get(self, key: str, nestedIn: list | None = None, defaultValue: Any = None):
        """ 
        Получение значения поля в конфиге.
        ----------------------------------
        @param key: Имя поля в конфиге.
        @param nestedIn: Список полей в которые данное поле вложено.
        Например для user.info.login: nestedIn = [user, info].
        @param defaultValue: Значение поля по умолчанию. \
            Будет возвращено, если поле не найдено. \
            Если defaultValue = None и поле не найдено, то метод выбрасывает ошибку.
        """
        try:
            data = self._pull(key, nestedIn)
            return data[key]
        except KeyError as error:
            if defaultValue is None:
                raise error
            return defaultValue

    def set(self, key: str, value, nestedIn: list | None = None):
        """Выставление значения поля в конфиге. Работает по аналогии с get."""

        data = self._pull(key, nestedIn)
        data[key] = value


@configField("contest-system", str)
@configField("login", str, nestedIn=["user"])
@configField("password", str, nestedIn=["user"])
@configField("name", str, nestedIn=["user"])
@configField("home-url", str)
@configField(
    "locale",
    str,
    serializer=lambda x: Locale[x],
    deserializer=lambda x: x.name,
    defaultValue=Locale.russian,
)
@configField("enable-auto-tests", bool, nestedIn=["features"], defaultValue=True)
@configField("enable-auto-formatting", bool, nestedIn=["features"], defaultValue=True)
@configField("debug", bool, defaultValue=False)
class GlobalConfig(Config):
    pass
