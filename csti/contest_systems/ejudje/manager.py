from typing import override

from csti.contest.manager import ContestManager
from csti.contest_systems.ejudje.api import ContestSystemAPI, EjudjeAPI


class EjudjeManager(ContestManager):
    def __init__(self):
        super().__init__()
        self._apis = {}

    @override
    def getAPI(self) -> ContestSystemAPI:
        return EjudjeAPI(0)

    @override
    def getAPIForContest(self, contestId: int) -> ContestSystemAPI:
        if contestId not in self._apis:
            self._apis[contestId] = EjudjeAPI(contestId)
        return self._apis[contestId]
