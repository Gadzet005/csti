import typing as t

from csti.cli.utils.print import Printer
from csti.contest.env import ContestEnv
from csti.contest.systems import ContestSystem
from csti.etc.consts import APP_NAME
from csti.storage.config import Config
from csti.storage.config.general import GeneralConfig


class ContestCLI:
    def __init__(
        self,
        config: t.Optional[Config] = None,
        env: t.Optional[ContestEnv] = None,
        printer: t.Optional[Printer] = None,
    ):
        self._config = config or GeneralConfig.forApp(APP_NAME)
        self._env = env or ContestEnv()

        self._config.create()
        self._config.load()

        useColor = self.config.get("use-color")
        self._printer = printer or Printer(noColor=not useColor)

    @property
    def config(self) -> Config:
        return self._config

    @property
    def print(self) -> Printer:
        return self._printer

    def getEnv(self, checkExists: bool = True) -> ContestEnv:
        if checkExists:
            self._env.assertInitialized()
        return self._env

    def createEnv(self, dir: t.Optional[str], system: ContestSystem):
        self._env = ContestEnv(dir)
        self._env.create(system)
