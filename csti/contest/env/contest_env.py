import os
import typing as t

from csti.contest import Contest, Task
from csti.contest.env.data_storage import EnvDataStorage
from csti.contest.env.exceptions import EnvNotInitialized, EnvError


class ContestEnv:
    """Управляет директорией для работы с контестом."""

    def __init__(
        self, 
        dir: t.Optional[str] = None, 
        assertInitialized: bool = True
    ):
        self._dir = dir or os.getcwd()
        self._storage = EnvDataStorage.forEnv(self._dir)

        if assertInitialized:
            self.assertInitialized()

    def init(self):
        """Инициализирует директорию для работы с контестом."""
        os.makedirs(self.dir, exist_ok=True)
        self.storage.create()

    @property
    def dir(self) -> str:
        return self._dir

    @property
    def storage(self) -> EnvDataStorage:
        return self._storage

    @property
    def isInitialized(self) -> bool:
        return os.path.exists(self.storage.dir)

    def assertInitialized(self):
        """
        Если директория не инициализирована, 
        выбрасывает исключение `EnvNotInitialized`.
        """
        if not self.isInitialized:
            raise EnvNotInitialized


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
