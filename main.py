from src.cli.cli import cli
from src.contest.contest_interface import ContestInterface
from src.config import ConfigManager 

if __name__ == "__main__":
	login = ConfigManager().login
	password = ConfigManager().password
	ContestInterface().signIn(login, password)
	cli()
