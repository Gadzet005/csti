import typing as t
from functools import cache

import requests

from csti.config.config import Config
from csti.contest.api import ContestSystemAPI
from csti.contest.exceptions import AuthException
from csti.contest_systems.ejudje.language import EjudjeLanguage
from csti.contest_systems.ejudje.parser import ContestParser, TaskParser


class EjudjeAPI(ContestSystemAPI):
    URL = "https://contest.solutions"
    REQUEST_URL = URL + "/cgi-bin/new-client"
    BAD_SESSION_ID = "0000000000000000"
    Lang = EjudjeLanguage

    def __init__(self, config: Config, contestId: t.Optional[int] = None):
        super().__init__(config, contestId)
        self._sessionId: str = ""
        self._cookieSessionId: str = ""

    @classmethod
    @cache
    @t.override
    def getInstance(cls, config: Config, contestId: t.Optional[int] = None) -> t.Self:
        return cls(config, contestId)

    def getSession(self) -> requests.Session:
        if not self._sessionId or not self._cookieSessionId:
            self._createSession()

        session = requests.Session()
        session.cookies.set("EJSID", self._cookieSessionId)
        return session

    def _createSession(self):
        login = self._config.get("user", "login")
        password = self._config.get("user", "password")
        locale = self._config.get("locale")

        contestInfo = self.getContestInfo()
        if contestInfo is None:
            raise AuthException(
                f"Не удалось получить доступ к контесту (id={self._contestId})."
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
                "locale_id": locale,
            },
        )

        sessionId = ContestParser.getSessionId(response.content)
        if sessionId == self.BAD_SESSION_ID:
            raise AuthException(
                "В доступе к контесту отказано. "
                "Проверьте номер контеста, логин и пароль."
            )

        ejsid = response.cookies.get("EJSID")
        if ejsid is None:
            raise AuthException("Не удалось получить EJSID.")

        self._cookieSessionId = ejsid
        self._sessionId = sessionId

    @cache
    def _getHomePage(self) -> bytes:
        response = requests.get(self._config.get("home-url"))
        return response.content

    @cache
    def _getContestIds(self) -> list[int]:
        homePage = self._getHomePage()
        return ContestParser.getContestLocalIds(homePage)

    @t.override
    def getContestIds(self) -> list[int]:
        return self._getContestIds()

    @cache
    def _getContestInfo(self) -> t.Optional[dict]:
        homePage = self._getHomePage()
        name = self._config.get("user", "name")

        info = ContestParser.getContestInfo(homePage, name, self.contestId)
        if info is None:
            return

        return {
            "name": f"Контест №{self._contestId}",
            "taskIds": info["taskIds"],
            "other": {
                "globalId": info["contestGlobalId"],
            },
        }

    @t.override
    def getContestInfo(self, *args) -> t.Optional[dict]:
        return self._getContestInfo()

    @cache
    def _getTaskInfo(self, taskId: int) -> t.Optional[dict]:
        session = self.getSession()

        response = session.get(
            self.REQUEST_URL,
            params={"SID": self._sessionId, "action": 139, "prob_id": taskId},
        )

        html = response.content
        name = TaskParser.getName(html)
        if name is None:
            return

        description = TaskParser.getCondition(html)
        inputExample = TaskParser.getTests(html)
        info = TaskParser.getInfo(html)
        lastSolution = TaskParser.getLastSolution(html)

        if info is None:
            return None

        solutions = []
        if lastSolution:
            solutions.append(
                {
                    "id": lastSolution.id,
                    "status": lastSolution.status.value,
                    "testsPassed": lastSolution.testsPassed,
                }
            )

        return {
            "name": name,
            "description": description,
            "inputExample": inputExample,
            "timeLimit": int(info["Ограничение времени"][:-2]),
            "memoryLimit": int(info["Ограничение памяти"][:-1]),
            "remainingAttempts": int(info["Оставшиеся посылки"]),
            "isSolved": False,
            "solutions": solutions,
            "languageIds": [EjudjeLanguage.nasm.id],
        }

    @t.override
    def getTaskInfo(self, contestId: int, taskId: int) -> t.Optional[dict]:
        return self._getTaskInfo(taskId)

    @t.override
    def sendTaskSolution(
        self, contestId: int, taskId: int, code: str, languageId: int
    ) -> bool:
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
                "action_40": "",
            },
        )

        # TODO: Сделать проверку.
        return True
