from csti.contest.manager import ContestManager
from csti.contest.systems.ejudje import EjudjeAPI
from csti.data_storage.config.config import Config


def getManager(config: Config) -> ContestManager:
    name = config.get("contest-system")
    match name:
        case "ejudje":
            return ContestManager(EjudjeAPI(config))
        case _:
            raise ValueError(f"Неизвестная система: {name}")
