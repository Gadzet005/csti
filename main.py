from src.cli.cli import cli
from src.config import login, password
from src.contest.contest_interface import ContestInterface

if __name__ == "__main__":
	ContestInterface().signIn(login, password)
	cli()
