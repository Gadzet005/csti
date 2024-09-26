from csti.contest.systems.contest_solutions import (ContestSolutionsAPI,
                                                    ContestSolutionsConfig,
                                                    ContestSolutionsConfigTuner)
from csti.contest.systems.contest_system import ContestSystem


class SupportedContestSystem(ContestSystem):
    contestSolutions = {
        "fullName": "Contest Solutions",
        "api": ContestSolutionsAPI,
        "config": ContestSolutionsConfig,
        "configTuner": ContestSolutionsConfigTuner,
    }
