from click.testing import CliRunner

from tests.testcase import IsolatedDirCase
from csti.cli.commands.root import root
from csti.cli import CLIApp
from tests.cli.config import config


class TestCLI(IsolatedDirCase):
    DATA_DIR = "cli"
    TEST_DIR = "cli/test"

    def testCLI(self):
        app = CLIApp("csti", config)
        state = app.getState()

        runner = CliRunner()
        # result = runner.invoke(root, ["init"], obj=state)
        # print(result.exit_code)
        # print("result =", result.output)
