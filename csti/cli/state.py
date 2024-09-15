import typing as t
from functools import cache

from csti.etc.app import App
from csti.cli.utils.print import Printer
from csti.contest.manager import ContestManager
from csti.contest_env import ContestEnv
from csti.config import Config


class CLIState:
    def __init__(
        self, 
        app: App,
        manager: ContestManager,
        printer: t.Optional[Printer] = None,
    ):
        self._app = app
        self._manager = manager
        self._printer: Printer = printer or Printer() # type: ignore

    @property
    def app(self) -> App:
        return self._app
    
    @property
    def config(self) -> Config:
        return self.app.config

    @property
    @cache
    def env(self) -> ContestEnv:
        return ContestEnv.inCurrentDir()

    @property
    def print(self) -> Printer:
        return self._printer
    
    @property
    def manager(self) -> ContestManager:
        return self._manager
