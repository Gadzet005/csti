from csti.contest.api import ContestSystemAPI
from csti.contest.task import Task


class Contest:
    def __init__(self, contestId: int, api: ContestSystemAPI):
        self._id = contestId
        self._api = api

    @property
    def id(self) -> int:
        return self._id

    @property
    def info(self) -> dict:
        return self._api.getContestInfo(self._id)

    @property
    def name(self) -> str:
        return self.info["name"]

    def getTasks(self) -> list[Task]:
        return [
            self.getTask(taskId)
            for taskId in self.info["tasks"]
        ]

    def getTask(self, taskId):
        return Task(taskId, self._api)
