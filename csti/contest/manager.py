import abc

from csti.config.config import Config
from csti.contest.api import ContestSystemAPI
from csti.contest.contest import Contest


class ContestManager(abc.ABC):
    def __init__(self, api: ContestSystemAPI):
        self._api = api

    def getContests(self, onlyValid: bool = True) -> list[Contest]:
        contestIds = self._api.getContestIds()
        contests = []

        for contestId in contestIds:
            contest = self.getContest(contestId)
            if not onlyValid or contest.isValid:
                contests.append(contest)

        return contests

    def getContest(self, contestId: int) -> Contest:
        return Contest(contestId, self._api)
