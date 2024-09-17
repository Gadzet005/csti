import typing as t

from csti.cli.commands.root import root
from csti.cli.state import CLIState
from csti.cli.utils.print import Printer
from csti.config import Config, GeneralConfig
from csti.contest.systems.manager import getManager
from csti.etc.app import RunableApp


class CLIApp(RunableApp):
    def __init__(
        self, 
        name: str, 
        config: t.Optional[Config] = None,
        printer: t.Optional[Printer] = None
    ):
        config = config or GeneralConfig.forApp(name)
        super().__init__(name, config)
        self._printer = printer or Printer()

    @t.override
    def _run(self):
        debug = self.config["debug"]
        manager = getManager(self.config)

        state = CLIState(self.config, manager, self._printer)

        try:
            root(obj=state)
        except Exception as error:
            if debug:
                raise error
            else:
                state.print.error(f"Ошибка выполнения: {error}")
