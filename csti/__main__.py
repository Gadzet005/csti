from csti.cli.app import CLIApp
from csti.etc.consts import APP_NAME, APP_VERSION


def main():
    app = CLIApp(APP_NAME, APP_VERSION)
    app.run()


if __name__ == "__main__":
    main()
