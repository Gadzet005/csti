from csti.contest.systems.contest_solutions import (ContestSolutionsAPI,
                                                    ContestSolutionsConfig,
                                                    ContestSolutionsConfigTuner)
from csti.contest.systems.ejudge_vmk_2kurs import (Ejudge2KursVmkAPI,
    Ejudge2KursVmkConfig, Ejudge2KursVmkConfigTuner)

from csti.contest.systems.contest_system import ContestSystem


class SupportedContestSystem(ContestSystem):
    contestSolutions = {
        "fullName": "Contest Solutions",
        "api": ContestSolutionsAPI,
        "config": ContestSolutionsConfig,
        "configTuner": ContestSolutionsConfigTuner,
    }

    ejudge = {
        "fullName": "Ejudge for vmk",
        "api": Ejudge2KursVmkAPI,
        "config": Ejudge2KursVmkConfig,
        "configTuner": Ejudge2KursVmkConfigTuner,
    }
