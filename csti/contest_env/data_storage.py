from __future__ import annotations

import os
from typing import Any, override

from csti.contest import Contest, Task
from csti.contest_env.exceptions import EnvStorageException
from csti.contest_systems import getManager
from csti.data_storage import DataStorage, Group, StorageTemplate
from csti.data_storage.exceptions import FieldNotInitialized
from csti.data_storage.field import IntField, ListField
from csti.etc.settings import APP_NAME


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

    @override
    @staticmethod
    def init(envDir: str, *args, **kwargs) -> EnvDataStorage:
        os.makedirs(os.path.join(envDir, EnvDataStorage.FOLDER), exist_ok=True)
        return EnvDataStorage(envDir)

    def getPathByLocation(self, location: list[str]):
        return os.path.join(self._dir, *location)

    @override
    def _get(self, location: list[str]) -> Any:
        try:
            with open(self.getPathByLocation(location), "r") as f:
                return f.read()
        except FileNotFoundError:
            raise FieldNotInitialized(location)

    @override
    def _set(self, location: list[str], value):
        path = self.getPathByLocation(location)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(str(value))

    @property
    def dir(self) -> str:
        return self._dir

    def loadContest(self) -> Contest:
        manager = getManager()
        try:
            id = self.get("contest", "id")
            return manager.getContest(id)
        except FieldNotInitialized:
            raise EnvStorageException("Контест не выбран.")

    def loadCurrentTask(self) -> Task:
        try:
            contest = self.loadContest()
            taskId = self.get("contest", "currentTaskId")
            return contest.getTask(taskId)
        except:
            raise EnvStorageException("Задача не выбрана.")
