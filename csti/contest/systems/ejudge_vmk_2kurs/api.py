import re
import typing as t
from functools import cache

import requests

from csti.contest.api import ContestSystemAPI
from csti.contest.systems.ejudge_vmk_2kurs.api_error import (APIException,
                                                             EjudgeAPIException)
from csti.contest.systems.ejudge_vmk_2kurs.language import \
    Ejudge2KursVmkLanguage
from csti.storage.config.config import Config


class Ejudge2KursVmkAPI(ContestSystemAPI):
    REQUEST_URL = "/cgi-bin/new-client"
    RESPONSE_ENCODING = "utf-8"
    Lang = Ejudge2KursVmkLanguage

    CONTEST_TYPES = {"mz": "Маш. зал.", "up": "Дореш."}

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

    def getSession(self) -> requests.Session:
        if not self._sid or not self._ejsid:
            self._createSession()

        session = requests.Session()
        session.params = {"SID": self._sid, "EJSID": self._ejsid, "json": True}
        return session

    def _createSession(self):
        login = self._config.get("login")
        password = self._config.get("password")

        response = requests.post(
            self.requestUrl,
            data={
                "contest_id": self._config.get("contest-id"),
                "login": login,
                "password": password,
                "action": "login-json",
                "json": True,
            },
        )

        data = self.getResponseJson(response)

        self._ejsid = data.get("EJSID", "invalid")
        self._sid = data.get("SID", "invalid")

    @cache
    def _getContestStatus(self) -> dict:
        session = self.getSession()
        response = session.get(
            self.requestUrl,
            params={
                "action": "contest-status-json",
            },
        )
        data = self.getResponseJson(response)
        return data

    @cache
    def _getTaskStatus(self, taskId: int) -> dict:
        session = self.getSession()
        response = session.get(
            self.requestUrl,
            params={
                "action": "problem-status-json",
                "problem": taskId,
            },
        )
        data = self.getResponseJson(response)
        return data

    @cache
    def _getTaskStatement(self, taskId: int) -> str:
        session = self.getSession()
        response = session.get(
            self.requestUrl,
            params={
                "action": "problem-statement-json",
                "problem": taskId,
            },
        )
        data = self.getResponseContent(response)
        return data

    @cache
    def _getTaskSolutions(self, taskId: int) -> dict:
        session = self.getSession()
        response = session.get(
            self.requestUrl,
            params={
                "action": "list-runs-json",
                "prob_id": taskId,
            },
        )
        data = self.getResponseJson(response)
        return data

    @cache
    def _getSolutionStatus(self, solutionId: int):
        session = self.getSession()
        response = session.get(
            self.requestUrl,
            params={
                "action": "run-status-json",
                "run_id": solutionId,
            },
        )
        data = self.getResponseJson(response)
        return data

    @cache
    def _getSolutionCode(self, solutionId: int) -> str:
        session = self.getSession()
        response = session.get(
            self.requestUrl,
            params={
                "action": "download-run",
                "run_id": solutionId,
            },
        )
        data = self.getResponseContent(response)
        return data

    def _submitSolution(self, taskId: int, code: str, languageId: int) -> dict:
        session = self.getSession()
        response = session.post(
            self.requestUrl,
            params={
                "action": "submit-run",
                "prob_id": taskId,
                "lang_id": languageId,
                "file": code,
            },
        )
        data = self.getResponseJson(response)
        return data

    def _getTaskGlobalIdFromLocal(self, contestId: int, taskId: int) -> int:
        problems = self._getContestStatus().get("problems")
        if problems is None:
            raise Exception("Не удалось полуить имена задач.")

        for problem in problems:
            if re.match(r"\w{2}\d*" + f"{contestId}-{taskId}", problem.get("short_name", "")) and self._getTaskStatus(problem["id"])["problem_status"]["is_viewable"] == 1:
                return int(problem["id"])

        raise Exception("Не удалось преобразовать локальное айди задачи в\
            глобальное.")
        

    @cache
    def _getContestInfo(self, contestId: int) -> t.Optional[dict]:
        data = dict()
        for contestType in self.CONTEST_TYPES.keys():
            data[contestType] = {
                "name": "",
                "isOpen": None,
                "taskIds": list(),
            }

        problems = self._getContestStatus().get("problems")
        if problems is None:
            raise  # Придумать ошибку.

        contestType = ""
        for problem in problems:
            shortProblemName = problem.get("short_name", "")
            problemContestId = int(
                re.findall(r"\w{2}(\d{2})-\d{1,}", shortProblemName)[0]
            )
            problemLocalId = int(
                re.findall(r"\w{2}\d{2}-(\d{1,})", shortProblemName)[0]
            )
            if problemContestId < contestId:
                continue

            elif problemContestId > contestId:
                break

            contestType = re.findall(r"(\w{2})\d{2}-\d{1,}", shortProblemName)[0]
            data[contestType]["taskIds"].append(problemLocalId)
            if data[contestType]["isOpen"] is None:
                data[contestType]["isOpen"] = bool(
                    self._getTaskStatus(problem["id"])["problem_status"]["is_viewable"]
                )

        if data[contestType]["isOpen"] is None:
            raise  # Придумать ошибку.

        data[contestType]["name"] = f"{self.CONTEST_TYPES[contestType]} {contestId}"

        return data[contestType]

    @cache
    def _getTaskInfo(self, contestId: int, taskId: int) -> t.Optional[dict]:
        taskId = self._getTaskGlobalIdFromLocal(contestId, taskId)
        problem = self._getTaskStatus(taskId).get("problem")
        description = self._getTaskStatement(taskId)
        solutions = self._getTaskSolutions(taskId).get("runs", list())
        solutions_out = list()
        for solution in solutions:
            solution_out = dict()
            solution_out["id"] = int(solution.get("run_id"))
            solution_out["testsPassed"] = solution.get("passed_tests")
            solution_out["submissionTime"] = None
            solution_out["status"] = solution.get("status")
            solution_out["code"] = None
            solutions_out.append(solution_out)

        if problem is None:
            raise  # TODO: Придумать ошибку.

        return {
            "name": problem.get("long_name"),
            "description": description,
            "inputFormat": None,
            "outputFormat": None,
            "inputExample": None,
            "timeLimit": int(problem.get("real_time_limit_ms")) / 1000,
            "memoryLimit": int(problem.get("max_rss_size")) / 1024**2,
            "remainingAttempts": None,
            "solutions": solutions_out,
            "isSolved": problem.get("is_solved", False),
            "languageIds": problem.get("compilers"),
        }

    @cache
    def _getContestIds(self) -> list[int]:
        problems = self._getContestStatus().get("problems")
        if problems is None:
            raise  # Придумать ошибку.

        contestIds = list()
        for problem in problems:
            shortProblemName = problem.get("short_name", "")
            contestId = int(re.findall(r"\w{2}(\d{2})-\d{1,}", shortProblemName)[0])
            if contestId not in contestIds:
                contestIds.append(contestId)

        return contestIds

    @t.override
    def getContestIds(self) -> list[int]:
        return self._getContestIds()

    @t.override
    def getContestInfo(self, contestId: int):
        return self._getContestInfo(contestId)

    @t.override
    def getTaskInfo(self, contestId: int, taskId: int) -> t.Optional[dict]:
        return self._getTaskInfo(contestId, taskId)

    @t.override
    def sendTaskSolution(
        self, contestId: int, taskId: int, code: str, languageId: int
    ) -> bool:
        taskId = self._getTaskGlobalIdFromLocal(contestId, taskId)
        try:
            self._submitSolution(taskId, code, languageId)
            return True
        except APIException:
            return False
