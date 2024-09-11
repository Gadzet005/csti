from functools import cache
from typing import override

import requests

from csti.config import GlobalConfig
from csti.contest.api import ContestSystemAPI
from csti.contest_systems.ejudje.language import EjudjeLanguage
from csti.contest_systems.ejudje.parser import ContestParser, TaskParser
from csti.contest.exceptions import AuthException, ParserError


class EjudjeAPI(ContestSystemAPI):
    URL = "https://contest.solutions"
    REQUEST_URL = URL + "/cgi-bin/new-client"
    BAD_SESSION_ID = "0000000000000000"
    Lang = EjudjeLanguage

    def __init__(self, contestId: int):
        self._contestId = contestId
        self._sessionId: str = ""
        self._cookieSessionId: str = ""

    def getSession(self) -> requests.Session:
        if not self._sessionId or not self._cookieSessionId:
            self._createSession()

        session = requests.Session()
        session.cookies.set("EJSID", self._cookieSessionId)
        return session

    def _createSession(self):
        login = GlobalConfig().login
        password = GlobalConfig().password
        locale = GlobalConfig().locale.value

        contestInfo = self.getContestInfo()
        if contestInfo is None:
            raise AuthException(
                "Не удалось получить доступ к информации о контесте. "
                "Проверьте home-url."
            )
        contestGlobalId = str(contestInfo["other"]["globalId"])
        
        response = requests.post(
            self.REQUEST_URL,
            headers={
                "Content-Type": "multipart/form-data",
            },
            data={
                "contest_id": contestGlobalId,
                "login": login,
                "password": password,
                "locale_id": locale
            }
        )

        sessionId = ContestParser.getSessionId(response.content)
        if sessionId == self.BAD_SESSION_ID:
            raise AuthException(
                "В доступе к контесту отказано. "
                "Проверьте номер контеста, логин и пароль."
            )

        self._sessionId = sessionId
        self._cookieSessionId = response.cookies.get("EJSID")

    @staticmethod
    @cache
    def _getHomePage() -> bytes:
        response = requests.get(GlobalConfig().homeUrl)
        return response.content
    

    @classmethod
    @cache
    def _getContestIds(cls) -> list[int]:
        homePage = cls._getHomePage()
        return ContestParser.getContestLocalIds(homePage)

    @classmethod
    @override
    def getContestIds(cls) -> list[int]:
        return cls._getContestIds()


    @cache
    def _getContestInfo(self) -> dict|None:
        homePage = self._getHomePage()
        name = GlobalConfig().name

        info = ContestParser.getContestInfo(homePage, name, self._contestId)
        if info is None:
            return

        return {
            "name": f"Контест №{self._contestId}",
            "taskIds": info["taskIds"],
            "other": {
                "globalId": info["contestGlobalId"],
            }
        }
    
    @override
    def getContestInfo(self, *args) -> dict|None:
        return self._getContestInfo()


    @cache
    def _getTaskInfo(self, taskId: int) -> dict|None:
        session = self.getSession()

        response = session.get(
            self.REQUEST_URL,
            params = {
                "SID": self._sessionId,
                "action": 139,
                "prob_id": taskId
            }
        )

        html = response.content
        name = TaskParser.getName(html)
        if name is None:
            return

        description = TaskParser.getCondition(html)
        inputExample = TaskParser.getTests(html)
        info = TaskParser.getInfo(html)
        lastSolution = TaskParser.getLastSolution(html)
        
        solutions = []
        if lastSolution:
            solutions.append({
                "id": lastSolution.id,
                "status": lastSolution.status.value,
                "testsPassed": lastSolution.testsPassed,
            })
        
        return {
            "name": name,
            "description": description,
            "inputExample": inputExample,
            "timeLimit": int(info["Ограничение времени"][:-2]),
            "memoryLimit": int(info["Ограничение памяти"][:-1]),
            "remainingAttemps": int(info["Оставшиеся посылки"]),
            "isSolved": False,
            "solutions": solutions,
            "languageIds": [self.Lang.nasm.id],
        }

    @override
    def getTaskInfo(self, taskId: int) -> dict|None:
        return self._getTaskInfo(taskId)


    @override
    def sendTaskSolution(self, taskId: int, code: str, languageId: int) -> bool:
        session = self.getSession()

        session.post(
            self.REQUEST_URL,
            headers={
                "Content-Type": "multipart/form-data",
            },
            data={
                "SID": self._sessionId,
                "prob_id": taskId,
                "lang_id": languageId,
                "file": code,
                "action_40": ""
            }
        )

        # TODO: Сделать проверку.
        return True
