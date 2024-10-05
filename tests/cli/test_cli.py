from click.testing import CliRunner

from csti.cli import ContestCLI
from csti.cli.commands.root import root
from csti.cli.utils.print import Printer
from csti.contest.env import ContestEnv
from tests.cli.config import TestConfig
from tests.testcase import IsolatedDirCase


class TestCLI(IsolatedDirCase):
    DATA_DIR = "cli"
    TEST_DIR = "cli/test"

    def testCLI(self):
        globalConfig = TestConfig({})
        printer = Printer(noColor=True)
        env = ContestEnv(self.getTestDir())

        cli = ContestCLI(globalConfig, env, printer)
        runner = CliRunner()
        result = runner.invoke(root, ["init"], obj=cli, input="\n")
