from csti.contest.manager import ContestManager
from csti.contest.systems.ejudje import EjudjeAPI
from csti.etc.app import App


def getManager(app: App) -> ContestManager:
    name = app.config.get("contest-system")
    match name:
        case "ejudje":
            return ContestManager(EjudjeAPI, app.config)
        case _:
            raise ValueError(f"Неизвестная система: {name}")
