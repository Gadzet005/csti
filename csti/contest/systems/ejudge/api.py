import typing as t
from functools import cache

import requests

from csti.contest.api import ContestSystemAPI
from csti.contest.systems.ejudge.api_error import (APIException,
                                                   EjudgeAPIException)
from csti.contest.systems.ejudge.language import EjudgeLanguage
from csti.storage.config.config import Config


class EjudgeAPI(ContestSystemAPI):
    REQUEST_URL = "/cgi-bin/new-client"
    RESPONSE_ENCODING = "utf-8"
    Lang = EjudgeLanguage

    _sessionCache: dict[int, tuple[str, str]] = {}

    def __init__(self, config: Config):
        super().__init__(config)
        self._sid: str = ""
        self._ejsid: str = ""

    @property
    def url(self):
        return self._config.get("url")
    
    @property
    def requestUrl(self):
        return self.url + self.REQUEST_URL
    
    @staticmethod
    def raiseResponseForStatus(response: requests.Response):
        if not response.ok:
            raise APIException(f"Ошибка запроса на сервер: {response.status_code}")

    @classmethod
    def getResponseContent(cls, response: requests.Response) -> str:
        cls.raiseResponseForStatus(response)
        return response.content.decode(cls.RESPONSE_ENCODING)

    @classmethod
    def getResponseJson(cls, response: requests.Response) -> dict:
        response.encoding = cls.RESPONSE_ENCODING
        cls.raiseResponseForStatus(response)

        json = response.json()
        if not json.get("ok", False):
            error = json.get("error", {})
            errorCode = error.get("symbol")
            message = error.get("message", "no message")
            raise EjudgeAPIException(errorCode, message)
    
        return json.get("result", {})

    def getSession(self, contestId: int) -> requests.Session:
        if not self._sid or not self._ejsid:
            if contestId in self._sessionCache:
                self._sid, self._ejsid = self._sessionCache[contestId]
            else:
                self._createSession(contestId)

        session = requests.Session()
        session.params = {
            "SID": self._sid,
            "EJSID": self._ejsid,
            "json": True
        }
        return session


    def _createSession(self, contestId: int):
        login = self._config.get("login")
        password = self._config.get("password")

        response = requests.post(
            self.requestUrl,
            data={
                "contest_id": contestId,
                "login": login,
                "password": password,
                "action": "login-json",
                "json": True,
            },
        )

        data = self.getResponseJson(response)

        self._ejsid = data.get("EJSID", "invalid")
        self._sid = data.get("SID", "invalid")
        self._sessionCache[contestId] = (self._sid, self._ejsid)
    
    @cache
    def _getContestStatus(self, contestId: int) -> dict:
        session = self.getSession(contestId)
        response = session.get(
            self.requestUrl,
            params = {
                "action": "contest-status-json",
            }
        )
        data = self.getResponseJson(response)
        return data

    @cache
    def _getTaskStatus(self, contestId: int, taskId: int) -> dict:
        session = self.getSession(contestId)
        response = session.get(
            self.requestUrl,
            params = {
                "action": "problem-status-json",
                "problem": taskId,
            }
        )
        data = self.getResponseJson(response)
        return data

    @cache
    def _getTaskDescription(self, contestId: int, taskId: int) -> str:
        session = self.getSession(contestId)
        response = session.get(
            self.requestUrl,
            params = {
                "action": "problem-statement-json",
                "problem": taskId,
            }
        )
        data = self.getResponseContent(response)
        return data

    @cache
    def _getTaskSolutions(self, contestId: int, taskId: int) -> dict:
        session = self.getSession(contestId)
        response = session.get(
            self.requestUrl,
            params = {
                "action": "list-runs-json",
                "prob_id": taskId,
            }
        )
        data = self.getResponseJson(response)
        return data

    @cache
    def _getSolutionStatus(self, contestId: int, solutionId: int):
        session = self.getSession(contestId)
        response = session.get(
            self.requestUrl,
            params = {
                "action": "run-status-json",
                "run_id": solutionId,
            }
        )
        data = self.getResponseJson(response)
        return data

    @cache
    def _getSolutionCode(self, contestId: int, solutionId: int) -> str:
        session = self.getSession(contestId)
        response = session.get(
            self.requestUrl,
            params = {
                "action": "download-run",
                "run_id": solutionId,
            }
        )
        data = self.getResponseContent(response)
        return data

    def _submitSolution(
        self, contestId: int, taskId: int, code: str, languageId: int
    ) -> dict:
        session = self.getSession(contestId)
        response = session.post(
            self.requestUrl,
            params = {
                "action": "submit-run",
                "prob_id": taskId,
                "lang_id": languageId,
                "file": code,
            }
        )
        data = self.getResponseJson(response)
        return data
    

    @t.override
    def getContestIds(cls) -> set[int]:
        return set()

    @t.override
    def getContestInfo(self, contestId: int) -> t.Optional[dict]:
        pass
    
    @t.override
    def getTaskInfo(self, contestId: int, taskId: int) -> t.Optional[dict]:
        pass

    @t.override
    def sendTaskSolution(
        self, contestId: int, taskId: int, code: str, languageId: int
    ) -> bool:
        try:
            self._submitSolution(contestId, taskId, code, languageId)
            return True
        except APIException:
            return False
