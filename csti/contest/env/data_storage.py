import os
import typing as t

from csti.contest import Contest, Task
from csti.contest.env.exceptions import EnvStorageException
from csti.contest.manager import ContestManager
from csti.data_storage import Group, StorageTemplate
from csti.data_storage.exceptions import FieldIsEmpty
from csti.data_storage.file import FileStorage
from csti.data_storage.file.field import IntField, ListField
from csti.etc.consts import APP_NAME


class EnvDataStorage(FileStorage):
    FOLDER = "." + APP_NAME
    template = StorageTemplate(
        [
            Group(
                "contest",
                [
                    IntField("id"),
                    IntField("currentTaskId"),
                    ListField("taskFiles", default=[], separator="\n"),
                ],
            )
        ]
    )

    @classmethod
    def fromEnv(cls, envDir: str) -> t.Self:
        return cls(os.path.join(envDir, cls.FOLDER))

    def loadContest(self, manager: ContestManager) -> Contest:
        try:
            id = self.get("contest", "id")
            return manager.getContest(id)
        except FieldIsEmpty:
            raise EnvStorageException("Контест не выбран.")

    def loadCurrentTask(self, manager: ContestManager) -> Task:
        try:
            contest = self.loadContest(manager)
            taskId = self.get("contest", "currentTaskId")
            return contest.getTask(taskId)
        except:
            raise EnvStorageException("Задача не выбрана.")
