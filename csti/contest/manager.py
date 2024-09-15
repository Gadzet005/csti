import abc
import typing as t

from csti.config.config import Config
from csti.contest.api import ContestSystemAPI
from csti.contest.contest import Contest


class ContestManager(abc.ABC):
    def __init__(self, apiType: t.Type[ContestSystemAPI], config: Config):
        self._apiType = apiType
        self._config = config

    def getContests(self, onlyValid: bool = True) -> list[Contest]:
        api = self._apiType.getInstance(self._config)
        contestIds = api.getContestIds()
        contests = []

        for contestId in contestIds:
            contest = self.getContest(contestId)
            if not onlyValid or contest.isValid:
                contests.append(contest)

        return contests

    def getContest(self, contestId: int) -> Contest:
        api = self._apiType.getInstance(self._config, contestId)
        return Contest(contestId, api)
