from csti.cli import cli
from csti.cli.print import cprint
from csti.config import GlobalConfig


def main():
    debug = GlobalConfig().debug

    try:
        cli()
    except Exception as error:
        if debug:
            raise error
        else:
            cprint.error(f"Ошибка выполнения: {error}")


if __name__ == "__main__":
    main()
