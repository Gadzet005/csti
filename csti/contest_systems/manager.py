from csti.config import GlobalConfig
from csti.contest.manager import ContestManager
from csti.contest_systems.ejudje import EjudjeAPI


def getManager() -> ContestManager:
    contestSystemName = GlobalConfig().contestSystem
    match contestSystemName:
        case "ejudje":
            return ContestManager(EjudjeAPI)
        case _:
            raise ValueError(f"Неизвестный менеджер контеста: {contestSystemName}")
