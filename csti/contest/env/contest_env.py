from __future__ import annotations

import os
import typing as t

from csti.contest import Contest, Task
from csti.contest.env.data_storage import EnvDataStorage
from csti.contest.env.exceptions import ContestEnvException


class ContestEnv:
    """Управляет папкой для работы с контестом."""

    def __init__(self, dir: str):
        self._dir = dir
        self._storage = EnvDataStorage(dir)

    @staticmethod
    def create(dir: t.Optional[str] = None) -> ContestEnv:
        """
        Инициализирует папку для работы с контестом.

        :param dir:
            Директория для инициализации.
            Если dir = `None`, то инициализирует текущую директорию.
        """
        dir = dir or os.getcwd()

        storage = EnvDataStorage(dir)
        storage.create()

        return ContestEnv(dir)

    def getTaskFile(self, task: Task) -> str:
        return str(task.id) + task.language.defaultfileExtension

    def clearTaskFiles(self):
        """Очистка файлов с заданиями."""

        taskFiles = self.storage.get("contest", "taskFiles")
        for file in taskFiles:
            path = os.path.join(self.dir, file)
            if os.path.isfile(path):
                os.remove(path)

    def createTaskFiles(self, tasks: list[Task], update: bool = False):
        """
        Создает файлы для заданий в рабочей директории.

        :param tasks: Список заданий.
        :param update: Дополнить существующие файлы - `True`, перезаписать - `False`.
        """

        taskFiles = []
        for task in tasks:
            file = self.getTaskFile(task)
            if os.path.exists(file):
                continue

            with open(os.path.join(self.dir, file), "w") as f:
                f.write(task.language.comment + " " + task.name + "\n")
                taskFiles.append(file)

        if update:
            taskFiles += self.storage.get("contest", "taskFiles")
        self.storage.set("contest", "taskFiles", value=taskFiles)

    def selectContest(self, contest: Contest):
        """Смена контеста в рабочей директории."""

        tasks = contest.getTasks()

        self.clearTaskFiles()
        self.createTaskFiles(tasks)
        self.storage.set("contest", "id", value=contest.id)
        self.storage.set("contest", "currentTaskId", value=tasks[0].id)

    @staticmethod
    def inCurrentDir() -> ContestEnv:
        """
        Проверяет, что рабочая (текущая) директория инициализирована
        и возвращает экземплер `ContestEnv`.
        """
        env = ContestEnv(os.getcwd())
        if not env.isEnvValid:
            raise ContestEnvException(
                "Рабочая папка не проинциализирована. Используйте csti init."
            )
        return env

    @property
    def dir(self) -> str:
        return self._dir

    @property
    def storage(self) -> EnvDataStorage:
        return self._storage

    @property
    def isEnvValid(self) -> bool:
        """Инициализирована ли рабочая директория?"""
        return os.path.exists(self.storage.dir)
