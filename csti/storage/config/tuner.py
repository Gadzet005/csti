import typing as t
import abc
from csti.storage.config import Config


class ConfigTuner(abc.ABC):
    """ Класс для настройки конфига через cli."""

    FieldName: t.TypeAlias = str | tuple[str, ...]

    def __init__(self, config: Config):
        self.config = config

    @abc.abstractmethod
    def _tune(self):
        pass

    def tune(self):
        self.config.load()
        self._tune()
        self.config.save()
