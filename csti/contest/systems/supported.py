from csti.contest.systems.contest_system import ContestSystem
from csti.contest.systems.ejudje import (EjudjeAPI, EjudjeConfig,
                                         EjudjeConfigTuner)


class SupportedContestSystem(ContestSystem):
    ejudje = {
        "fullName": "Ejudje",
        "api": EjudjeAPI,
        "config": EjudjeConfig,
        "configTuner": EjudjeConfigTuner,
    }
