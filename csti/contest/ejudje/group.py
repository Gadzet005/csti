from functools import cache
from typing import override

import requests

from csti.config.config import GlobalConfig
from csti.contest.ejudje.contest import EjudjeContest
from csti.contest.ejudje.api import EjudjeAPI
from csti.contest.ejudje.language import EjudjeLanguage
from csti.contest.ejudje.parser import ContestParser
from csti.contest.group import ContestGroup
from csti.etc.language import ILanguage


class EjudjeGroup(ContestGroup):
    @cache
    def _getContests(self) -> list[EjudjeContest]:
        homePage = requests.get(GlobalConfig().homeUrl).content
        ids = ContestParser.getContestLocalIds(homePage)
        raw = [self.getContest(id) for id in ids]
        return list(filter(lambda x: x is not None, raw))

    @override
    def getContests(self) -> list[EjudjeContest]:
        return self._getContests()
    
    @override
    def getContest(self, contestId: int) -> EjudjeContest|None:
        contest = EjudjeContest(contestId, EjudjeAPI(contestId))
        if contest.isValid:
            return contest

    @override
    def getAvailableLanguages(self) -> list[ILanguage]:
        return [EjudjeLanguage.nasm, EjudjeLanguage.c]
