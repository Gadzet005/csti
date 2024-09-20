from csti.cli import ContestCLI, root


def main():
    cli = ContestCLI.init()
    debug = cli.config.get("debug")

    try:
        root(obj=cli)
    except Exception as error:
        if debug:
            raise error
        else:
            cli.print.error(f"Ошибка выполнения: {error}")


if __name__ == "__main__":
    main()
