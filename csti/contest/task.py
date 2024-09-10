from csti.contest.api import ContestSystemAPI
from csti.program_view import ProgramView


class Task:
    def __init__(self, id: int, api: ContestSystemAPI):
        self._id = id
        self._api = api

    @property
    def id(self) -> int:
        return self._id
    
    @property
    def name(self) -> str:
        return self._api.getTaskInfo(self._id)["name"]
    
    @property
    def description(self) -> str:
        return self._api.getTaskInfo(self._id)["description"]
    
    @property
    def inputFormat(self) -> str:
        return self._api.getTaskInfo(self._id)["inputFormat"]
    
    @property
    def outputFormat(self) -> str:
        return self._api.getTaskInfo(self._id)["outputFormat"]
    
    @property
    def inputExample(self) -> list[tuple[str, str]]:
        return self._api.getTaskInfo(self._id)["inputExample"]
    
    @property
    def timeout(self) -> int:
        return self._api.getTaskInfo(self._id)["timeout"]
    
    @property
    def memoryLimit(self) -> int:
        return self._api.getTaskInfo(self._id)["memoryLimit"]
    
    @property
    def remainingAttempts(self) -> int:
        return self._api.getTaskInfo(self._id)["remainingAttempts"]
    
    @property
    def solutions(self) -> list:
        pass

    @property
    def isSolved(self) -> bool:
        return self._api.getTaskInfo(self._id)["isSolved"]
    @property
    def restrictions(self) -> str:
        return self._api.getTaskInfo(self._id)["restrictions"]

    def sendSolution(self, solution: ProgramView):
        self._api.sendTaskSolution(self._id, solution)
