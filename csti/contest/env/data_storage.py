import os
import typing as t

from csti.contest import Contest, Task
from csti.contest.manager import ContestManager
from csti.contest.env.exceptions import EnvStorageException
from csti.data_storage import DataStorage, Group, StorageTemplate
from csti.data_storage.exceptions import FieldNotInitialized
from csti.data_storage.field import IntField, ListField
from csti.etc.consts import APP_NAME


class EnvDataStorage(DataStorage):
    FOLDER = "." + APP_NAME
    template = StorageTemplate(
        [
            Group(
                "contest",
                [
                    IntField("id"),
                    IntField("currentTaskId"),
                    ListField("taskFiles", defaultValue=[], separator="\n"),
                ],
            )
        ]
    )

    def __init__(self, envDir: str):
        super().__init__()
        self._dir = os.path.join(envDir, self.FOLDER)

    @t.override
    def create(self):
        os.makedirs(self.dir, exist_ok=True)

    def getPathByLocation(self, location: tuple[str, ...]):
        return os.path.join(self._dir, *location)

    @t.override
    def _get(self, location: tuple[str, ...]) -> t.Any:
        try:
            with open(self.getPathByLocation(location), "r") as f:
                return f.read()
        except FileNotFoundError:
            raise FieldNotInitialized(location)

    @t.override
    def _set(self, location: tuple[str, ...], value):
        path = self.getPathByLocation(location)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(str(value))

    @property
    def dir(self) -> str:
        return self._dir

    def loadContest(self, manager: ContestManager) -> Contest:
        try:
            id = self.get("contest", "id")
            return manager.getContest(id)
        except FieldNotInitialized:
            raise EnvStorageException("Контест не выбран.")

    def loadCurrentTask(self, manager: ContestManager) -> Task:
        try:
            contest = self.loadContest(manager)
            taskId = self.get("contest", "currentTaskId")
            return contest.getTask(taskId)
        except:
            raise EnvStorageException("Задача не выбрана.")
