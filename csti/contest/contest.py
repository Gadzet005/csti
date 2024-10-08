import typing as t

from csti.contest.api import ContestSystemAPI
from csti.contest.exceptions import ContestException
from csti.contest.task import Task


class Contest:
    def __init__(self, contestId: int, api: ContestSystemAPI):
        self._id = contestId
        self._api = api

    @property
    def id(self) -> int:
        return self._id

    @property
    def _info(self) -> t.Optional[dict]:
        return self._api.getContestInfo(self._id)

    @property
    def isValid(self) -> bool:
        return self._info is not None

    @property
    def info(self) -> dict:
        if not self.isValid:
            raise ContestException(
                f"Попытка обращения к полям невалидного контеста (id={self._id})."
            )
        return self._info  # type: ignore

    @property
    def name(self) -> str:
        return self.info["name"]

    def getTasks(self, onlyValid: bool = True) -> list[Task]:
        tasks = []
        for taskId in self.info["taskIds"]:
            task = self.getTask(taskId)
            if not onlyValid or task.isValid:
                tasks.append(task)
        return tasks

    def getTask(self, taskId: int) -> Task:
        return Task(taskId, self._id, self._api)

    def __str__(self) -> str:
        return self.name
