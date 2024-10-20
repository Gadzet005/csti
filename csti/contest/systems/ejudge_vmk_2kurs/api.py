import datetime
import os
import re
import subprocess
import time
import typing as t
from functools import cache
from io import text_encoding

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

    @staticmethod
    def _safeUnparseIp(ipUnparse: str) -> str | None:
        ipParse = re.findall(r"(\d+.\d+.\d+.\d+)", ipUnparse)
        return ipParse[0] if len(ipParse) == 1 else None

    def _submitSolution(
        self, contestId: int, taskId: int, code: str, languageId: int
    ) -> dict:
        taskInfo = self.getTaskInfo(contestId, taskId)
        if taskInfo is None:
            raise Exception("Ошибка получения имени задачи.")

        mode = "r+"
        if not os.path.exists("ip"):
            mode = "w+"
        with open("ip", mode) as file:
            unparseIp = file.read()
            ip = self._safeUnparseIp(unparseIp)
            lastFileDateEdit = datetime.datetime.fromtimestamp(
                os.stat("ip").st_mtime
            ).day
            if ip is None or datetime.datetime.today().day - lastFileDateEdit >= 1:
                unparseIp = input("Введите IP адресс на сегодня: ")
                ip = self._safeUnparseIp(unparseIp)
                if ip is None:
                    raise Exception("Введен некоректный IP.")
                file.write(ip)

        addres = f"{self._config.get("login")}@{ip}"

        contestExsist = bool(
            subprocess.run(
                [
                    "ssh",
                    addres,
                    "[",
                    "-d",
                    "contest/521",
                    "]",
                    "&&",
                    "echo",
                    "True",
                    "||",
                    "echo",
                    "False",
                ],
                capture_output=True,
                text=True,
            ).stdout
        )

        if contestExsist == False:
            print("Монтируем ejudge-fuse в contest.")
            subprocess.run(
                [
                    "ssh",
                    addres,
                    "/opt/ejudge/bin/ejudge-fuse",
                    "--user",
                    self._config.get("login"),
                    "--password",
                    self._config.get("password"),
                    "--url",
                    f"{self._config.get("url")}/",
                    "~/contest",
                    "-ouse_ino",
                ]
            )

        sendFileName = "send-cashe.c"
        with open(sendFileName, "w") as file:
            file.write(code)

        subprocess.run(
            [
                "scp",
                sendFileName,
                f"{addres}:contest/521/problems/{taskInfo['name']}/submit/gcc/",
            ]
        )
        os.remove(sendFileName)

        return dict()

    def _getTaskGlobalIdFromLocal(self, contestId: int, taskId: int) -> int:
        problems = self._getContestStatus().get("problems")
        if problems is None:
            raise Exception("Не удалось полуить имена задач.")

        for problem in problems:
            if (
                re.match(
                    r"\w{2}\d*" + f"{contestId}-{taskId}", problem.get("short_name", "")
                )
                and self._getTaskStatus(problem["id"])["problem_status"]["is_viewable"]
                == 1
            ):
                return int(problem["id"])

        raise Exception(
            "Не удалось преобразовать локальное айди задачи в\
            глобальное."
        )

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
            "name": problem.get("short_name"),
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
        try:
            self._submitSolution(contestId, taskId, code, languageId)
            return True
        except APIException:
            return False
