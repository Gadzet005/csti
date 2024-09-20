import typing as t

from csti.cli.utils.print import Printer
from csti.config import GeneralConfig
from csti.contest.env import ContestEnv
from csti.contest.manager import ContestManager
from csti.contest.systems import ContestSystem
from csti.data_storage.config import Config
from csti.etc.consts import APP_NAME


class ContestCLI:
    def __init__(
        self,
        config: Config,
        manager: ContestManager,
        printer: t.Optional[Printer] = None,
    ):
        self._config = config
        self._manager = manager
        self._printer = printer or Printer()

    @classmethod
    def init(cls):
        config = GeneralConfig.forApp(APP_NAME)
        config.create()
        config.load()

        contestSystem: ContestSystem = config.get("contest-system")
        return cls(config, ContestManager(contestSystem.api))

    @property
    def config(self) -> Config:
        return self._config

    @property
    def print(self) -> Printer:
        return self._printer

    @property
    def manager(self) -> ContestManager:
        return self._manager

    def getEnv(
        self, 
        dir: t.Optional[str] = None, 
        assertInitialized: bool = True
    ):
        return ContestEnv(dir, assertInitialized)
