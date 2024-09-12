from csti.contest.api import ContestSystemAPI
from csti.contest.exceptions import APIException, TaskException
from csti.etc.language import ILanguage
from csti.program_view import ProgramView


class Task:
    def __init__(self, id: int, contestId: int, api: ContestSystemAPI):
        self._id = id
        self._contestId = contestId
        self._api = api

    @property
    def id(self) -> int:
        return self._id

    @property
    def _info(self) -> dict:
        return self._api.getTaskInfo(self._contestId, self._id)

    @property
    def isValid(self) -> bool:
        return self._info is not None

    @property
    def info(self) -> dict:
        if not self.isValid:
            raise TaskException(
                f"Попытка обращения к полям невалидной задачи (id={self._id})."
            )
        return self._info

    @property
    def name(self) -> str:
        return self.info["name"]

    @property
    def description(self) -> str:
        return self.info["description"]

    @property
    def inputFormat(self) -> str:
        return self.info["inputFormat"]

    @property
    def outputFormat(self) -> str:
        return self.info["outputFormat"]

    @property
    def inputExample(self) -> list[tuple[str, str]]:
        return self.info["inputExample"]

    @property
    def timeLimit(self) -> int:
        return self.info["timeLimit"]

    @property
    def memoryLimit(self) -> int:
        return self.info["memoryLimit"]

    @property
    def remainingAttempts(self) -> int:
        return self.info["remainingAttempts"]

    @property
    def solutions(self) -> list:
        return self.info["solutions"]

    @property
    def isSolved(self) -> bool:
        return self.info["isSolved"]

    @property
    def restrictions(self) -> str:
        return self.info["restrictions"]

    @property
    def languageIds(self) -> list:
        return self.info["languageIds"]

    @property
    def language(self) -> ILanguage:
        langId = self.languageIds[0]
        lang = self._api.Lang.fromId(langId)
        if lang is None:
            raise APIException(f"Неизвестный язык с id={langId}")
        return lang

    def sendSolution(self, solution: ProgramView):
        self._api.sendTaskSolution(
            self._contestId, self._id, solution.code, solution.lang.id
        )
