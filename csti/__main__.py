from csti.cli import cli
from csti.contest import ContestInterface


def main():
	ContestInterface().init()
	cli()

if __name__ == "__main__":
	main()
