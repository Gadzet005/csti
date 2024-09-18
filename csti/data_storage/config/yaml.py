import typing as t
import yaml

from csti.data_storage.config.config import Config
from csti.data_storage.exceptions import SaveError, LoadError


class YAMLConfig(Config):
    @t.override
    def save(self):
        try:
            with open(self.path, "w") as file:
                yaml.dump(self._data, file, allow_unicode=True, sort_keys=False)
        except OSError:
            raise SaveError(f"Не удалось сохранить данные в файл '{self.path}'.")

    @t.override
    def load(self):
        try:
            with open(self._path, "r") as file:
                self._data = yaml.safe_load(file)
        except OSError:
            raise LoadError(f"Не удалось загрузить данные из файла '{self.path}'.")
        except yaml.YAMLError as e:
            raise LoadError(f"Ошибка при загрузке файла '{self.path}': {e}")
    
    def create(self):
        with open(self.path, "w"):
            pass
