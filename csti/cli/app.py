import typing as t

import click

from csti.cli.commands.root import root
from csti.cli.state import CLIState
from csti.config.config import Config
from csti.config.global_config import GlobalConfig
from csti.contest_systems.manager import getManager
from csti.etc.app import RunableApp


class CLIApp(RunableApp):
    def __init__(
        self, 
        name: str,
        version: str, 
        config: t.Optional[Config]=None
    ):
        config = config or GlobalConfig.forApp(name)
        super().__init__(name, version, config)

    @t.override
    def _run(self):
        debug = self.config.get("debug")
        manager = getManager(self)
        state = CLIState(self, manager)

        try:
            root(obj=state)
        except Exception as error:
            if debug:
                raise error
            else:
                state.print.error(f"Ошибка выполнения: {error}")
