import typing as t
from functools import cache

from csti.cli.utils.print import Printer
from csti.contest.env import ContestEnv
from csti.contest.manager import ContestManager
from csti.data_storage.config import Config


class CLIState:
    def __init__(
        self,
        config: Config,
        manager: ContestManager,
        printer: t.Optional[Printer] = None,
    ):
        self._config = config
        self._manager = manager
        self._printer: Printer = printer or Printer()

    @property
    def config(self) -> Config:
        return self._config

    @property
    @cache
    def env(self) -> ContestEnv:
        return ContestEnv.inCurrentDir()

    def createEnv(self, dir: t.Optional[str] = None):
        return ContestEnv.create(dir)

    @property
    def print(self) -> Printer:
        return self._printer

    @property
    def manager(self) -> ContestManager:
        return self._manager
