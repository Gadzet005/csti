from cli import cli
from contest.contest_interface import ContestInterface
from config import ConfigManager 

if __name__ == "__main__":
	login = ConfigManager().login
	password = ConfigManager().password
	ContestInterface().signIn(login, password)
	cli()
