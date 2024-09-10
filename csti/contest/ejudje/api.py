from functools import cache
from typing import override

import requests

from csti.config import GlobalConfig
from csti.contest.api import ContestSystemAPI
from csti.contest.ejudje.language import EjudjeLanguage
from csti.contest.ejudje.parser import ContestParser, TaskParser
from csti.contest.exceptions import AuthException
from csti.etc.language import Language


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
    def getHomePage() -> bytes:
        response = requests.get(GlobalConfig().homeUrl)
        return response.content
    
    @cache
    def _getContestInfo(self) -> dict:
        homePage = self.getHomePage()
        name = GlobalConfig().name
        info = ContestParser.getContestInfo(homePage, name, self._contestId)
        
        if info["isValid"]:
            return {
                "name": f"Контест №{self._contestId}",
                "tasks": info["tasks"],
                "other": {
                    "globalId": info["contestGlobalId"],
                    "isValid": True
                }
            }
        else:
            return { "other": { "isValid": False } }
    
    @override
    def getContestInfo(self, *args) -> dict:
        return self._getContestInfo()

    @cache
    def _getTaskInfo(self, taskId: int) -> dict:
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
        info = TaskParser.getInfo(html)
        
        solutions = []
        lastSoltion = TaskParser.getLastSolution(html)
        if lastSoltion:
            solutions.append({
                "id": lastSoltion.id,
                "status": lastSoltion.status.value,
                "testsPassed": lastSoltion.testsPassed,
            })
        
        return {
            "name": TaskParser.getName(html),
            "description": TaskParser.getCondition(html),
            "inputExample": TaskParser.getTests(html),
            "timeLimit": int(info["Ограничение времени"][:-2]),
            "memoryLimit": int(info["Ограничение памяти"][:-1]),
            "remainingAttemps": int(info["Оставшиеся посылки"]),
            "isSolved": False,
            "solutions": solutions
        }

    @override
    def getTaskInfo(self, taskId: int) -> dict:
        return self._getTaskInfo(taskId)

    @override
    def sendTaskSolution(self, taskId: int, code: str, languageId: int):
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
