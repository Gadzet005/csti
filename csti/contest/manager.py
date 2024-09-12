import abc
from typing import Type

from csti.contest.contest import Contest
from csti.contest.api import ContestSystemAPI


class ContestManager(abc.ABC):
    def __init__(self, apiType: Type[ContestSystemAPI]):
        self._apiType = apiType

    def getContests(self, onlyValid: bool = True) -> list[Contest]:
        api = self._apiType.getInstance()
        contestIds = api.getContestIds()
        contests = []

        for contestId in contestIds:
            contest = self.getContest(contestId)
            if not onlyValid or contest.isValid:
                contests.append(contest)

        return contests

    def getContest(self, contestId: int) -> Contest:
        api = self._apiType.getInstance(contestId)
        return Contest(contestId, api)
