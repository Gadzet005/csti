from csti.cli.app import CLIApp
from csti.etc.consts import APP_NAME


def main():
    app = CLIApp(APP_NAME)
    app.run()


if __name__ == "__main__":
    main()
