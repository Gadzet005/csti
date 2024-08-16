from src.cli.cli import cli
from src.contest.contest_interface import ContestInterface
from src.config import getSignInData


if __name__ == "__main__":
	login, password = getSignInData()
	ContestInterface().signIn(login, password)
	cli()
