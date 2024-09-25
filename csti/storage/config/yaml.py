import typing as t

import yaml

from csti.storage.config.config import Config
from csti.storage.exceptions import LoadError, SaveError


class YAMLConfig(Config):
    @t.override
    def save(self):
        try:
            with open(self.path, "w") as file:
                yaml.dump(self._data, file, allow_unicode=True, sort_keys=False)
        except OSError:
            raise SaveError(f"Не удалось сохранить данные в файл '{self.path}'.")

    @t.override
    def load(self, force: bool = False):
        super().load(force)
        try:
            with open(self._path, "r") as file:
                self._data = yaml.safe_load(file) or {}
        except OSError:
            raise LoadError(f"Не удалось загрузить данные из файла '{self.path}'.")
        except yaml.YAMLError as e:
            raise LoadError(f"Ошибка при загрузке файла '{self.path}': {e}")
