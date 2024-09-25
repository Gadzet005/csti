import os
import typing as t

from csti.contest import Contest, Task
from csti.contest.env.data_storage import EnvDataStorage
from csti.contest.env.exceptions import EnvNotInitialized
from csti.contest.manager import ContestManager
from csti.contest.systems import ContestSystem
from csti.etc.consts import APP_NAME
from csti.storage.config import Config
from csti.storage.config.tuner import ConfigTuner


class ContestEnv:
    """Управляет директорией для работы с контестом."""

    DATA_DIR = "." + APP_NAME
    CONFIG_FILE = "config.yaml"

    def __init__(self, dir: t.Optional[str] = None):
        self._dir = dir or os.getcwd()
        self._storage = EnvDataStorage(self.dataDir)

    def create(self, system: ContestSystem):
        """Инициализирует директорию для работы с контестом."""

        os.makedirs(self.dataDir, exist_ok=True)
        self.storage.create()
        self.storage["contest-system"] = system
        self.getConfig().create()

    @property
    def dir(self) -> str:
        return self._dir

    @property
    def dataDir(self) -> str:
        return os.path.join(self.dir, self.DATA_DIR)

    @property
    def storage(self) -> EnvDataStorage:
        return self._storage

    @property
    def isInitialized(self) -> bool:
        return os.path.exists(self.dataDir)

    def assertInitialized(self):
        """
        Если директория не инициализирована,
        выбрасывает исключение `EnvNotInitialized`.
        """
        if not self.isInitialized:
            raise EnvNotInitialized

    @property
    def system(self) -> ContestSystem:
        return self.storage.get("contest-system")

    def getConfig(self) -> Config:
        path = os.path.join(self.dataDir, self.CONFIG_FILE)
        config = self.system.config(path)
        return config

    def getConfigTuner(self) -> ConfigTuner:
        return self.system.configTuner(self.getConfig())

    def getContestManager(self) -> ContestManager:
        return ContestManager(self.system.api(self.getConfig()))

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
        self.storage["contest", "taskFiles"] = taskFiles

    def selectContest(self, contest: Contest):
        """Смена контеста в рабочей директории."""

        tasks = contest.getTasks()

        self.clearTaskFiles()
        self.createTaskFiles(tasks)
        self.storage["contest", "id"] = contest.id
        self.storage["contest", "currentTaskId"] = tasks[0].id
