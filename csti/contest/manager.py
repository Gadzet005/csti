import abc

from csti.contest.contest import Contest
from csti.contest.api import ContestSystemAPI


class ContestManager(abc.ABC):
    @abc.abstractmethod
    def getAPI(self) -> ContestSystemAPI:
        """ Получение API. """
        pass
    
    def getAPIForContest(self, contestId: int) -> ContestSystemAPI:
        """ Получение API конкретного контеста. """
        return self.getAPI()

    def getContests(self, onlyValid: bool = True) -> list[Contest]:
        contestIds = self.getAPI().getContestIds()
        contests = []

        for contestId in contestIds:
            contest = self.getContest(contestId)
            if not onlyValid or contest.isValid:
                contests.append(contest)

        return contests

    def getContest(self, contestId: int) -> Contest:
        return Contest(contestId, self.getAPIForContest(contestId))
