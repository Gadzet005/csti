import typing as t
from enum import Enum

from csti.contest.api import ContestSystemAPI
from csti.storage.config import Config
from csti.storage.config.tuner import ConfigTuner


class ContestSystem(Enum):
    """ Перечисление доступных систем. """

    @property
    def fullName(self) -> str:
        return self.value["fullName"]
    
    @property
    def api(self) -> t.Type[ContestSystemAPI]:
        return self.value["api"]
    
    @property
    def config(self) -> t.Type[Config]:
        return self.value["config"]
    
    @property
    def configTuner(self) -> t.Type[ConfigTuner]:
        return self.value["configTuner"]
