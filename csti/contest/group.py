import abc

from csti.etc.language import ILanguage
from csti.contest.contest import Contest


class ContestGroup(abc.ABC):
    @abc.abstractmethod
    def getContests(self) -> list[Contest]:
        pass

    def getContest(self, contestId: int) -> Contest:
        pass

    @abc.abstractmethod
    def getAvailableLanguages(self) -> list[ILanguage]:
        pass
