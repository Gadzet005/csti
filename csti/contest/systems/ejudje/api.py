import typing as t
from functools import cache

import requests

from csti.config.config import Config
from csti.contest.api import ContestSystemAPI
from csti.contest.exceptions import AuthException
from csti.contest.systems.ejudje.language import EjudjeLanguage
from csti.contest.systems.ejudje.parser import ContestParser, TaskParser


class EjudjeAPI(ContestSystemAPI):
    URL = "https://contest.solutions"
    REQUEST_URL = URL + "/cgi-bin/new-client"
    BAD_SESSION_ID = "0000000000000000"
    Lang = EjudjeLanguage

    _sessionCache: dict[int, tuple[str, str]] = {}

    def __init__(self, config: Config):
        super().__init__(config)
        self._sessionId: str = ""
        self._cookieSessionId: str = ""

    def getSession(self, contestId: int) -> requests.Session:
        if not self._sessionId or not self._cookieSessionId:
            if contestId in self._sessionCache:
                self._sessionId, self._cookieSessionId = self._sessionCache[contestId]
            else:
                self._createSession(contestId)

        session = requests.Session()
        session.cookies.set("EJSID", self._cookieSessionId)
        return session

    def _createSession(self, contestId: int):
        login = self._config.get("user", "login")
        password = self._config.get("user", "password")
        locale = self._config.get("locale")

        contestInfo = self.getContestInfo(contestId)
        if contestInfo is None:
            raise AuthException(
                f"Не удалось получить доступ к контесту (id={contestId})."
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
        self._sessionCache[contestId] = (sessionId, ejsid)

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
    def _getContestInfo(self, contestId: int) -> t.Optional[dict]:
        homePage = self._getHomePage()
        name = self._config.get("user", "name")

        info = ContestParser.getContestInfo(homePage, name, contestId)
        if info is None:
            return

        return {
            "name": f"Контест №{contestId}",
            "taskIds": info["taskIds"],
            "other": {
                "globalId": info["contestGlobalId"],
            },
        }

    @t.override
    def getContestInfo(self, contestId: int) -> t.Optional[dict]:
        return self._getContestInfo(contestId)

    @cache
    def _getTaskInfo(self, contestId: int, taskId: int) -> t.Optional[dict]:
        session = self.getSession(contestId)

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
        return self._getTaskInfo(contestId, taskId)

    @t.override
    def sendTaskSolution(
        self, contestId: int, taskId: int, code: str, languageId: int
    ) -> bool:
        session = self.getSession(contestId)

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

        # TODO: Информация о результате отправки.
        return True
