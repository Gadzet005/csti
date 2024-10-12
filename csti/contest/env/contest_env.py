import os
import typing as t

from csti.contest import Contest, Task
from csti.contest.env.exceptions import EnvNotInitialized
from csti.contest.env.storage import EnvDataStorage
from csti.contest.env.task_file import TaskFile
from csti.contest.manager import ContestManager
from csti.contest.systems import ContestSystem
from csti.etc.consts import APP_NAME
from csti.storage.config import Config
from csti.storage.config.general import GeneralConfig
from csti.storage.config.tuner import ConfigTuner


class ContestEnv:
    """Управляет директорией для работы с контестом."""

    DATA_DIR = "." + APP_NAME
    STORAGE_DIR = "storage"
    CONFIG_FILE = "config.yaml"

    def __init__(self, config: GeneralConfig, dir: t.Optional[str] = None):
        self._config = config
        self._dir = dir or os.getcwd()
        self._storage = EnvDataStorage(os.path.join(self.dataDir, self.STORAGE_DIR))

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

    def getTaskFile(self, dir: str, task: Task) -> TaskFile:
        return TaskFile(self._config, dir, task)

    # def addTaskFile(self, task: Task):
    #     """
    #     Создает файл для задания в рабочей директории и
    #     добавляет его в список заданий.
    #     """

    #     tasks = self.storage["contest", "taskIds"]

    #     if task.id not in tasks:
    #         taskFile = self.getTaskFile(task)
    #         taskFile.create()
    #         tasks.append(task.id)

    #     self.storage["contest", "taskIds"] = tasks

    def selectContest(self, contest: Contest):
        """Смена контеста в рабочей директории."""

        oldTasks = self.storage.loadTasks(self.getContestManager())
        contestDirName = self._config.get("directories", "contest-dir-template",
                                          default="#")
        if not "#" in contestDirName:
            contestDirName += "#"

        if len(oldTasks) > 0 and self._config.get("directories", "archive-dir") != "./":
            oldTaskSavePath = f"{self.dir}/{self._config.get("directories", "archive-dir", default=self.DATA_DIR)}/{contestDirName}/"
            oldTaskSavePath = oldTaskSavePath.replace("#",
                                                      str(self.storage["contest",
                                                          "id"]))
            os.makedirs(oldTaskSavePath, exist_ok=True)
            for task in oldTasks:
                taskFile = self.getTaskFile(oldTaskSavePath, task)
                if os.path.exists(taskFile.path):
                    os.rename(
                        taskFile.path,
                        f"{oldTaskSavePath}{taskFile.name}",
                    )

        tasks = contest.getTasks()
        taskSavePath = f"{self.dir}/{contestDirName}/"
        taskSavePath = taskSavePath.replace("#", str(contest.id))
        os.makedirs(taskSavePath, exist_ok=True)
        for task in tasks:
            taskFile = self.getTaskFile(taskSavePath, task)
            if os.path.exists(f"{taskSavePath}{os.path.basename(taskFile.path)}"):
                os.rename(
                    f"{taskSavePath}{taskFile.name}", taskFile.path
                )
            else:
                taskFile.create()

        self.storage["contest", "taskIds"] = [task.id for task in tasks]
        self.storage["contest", "id"] = contest.id
        self.storage["contest", "currentTaskId"] = tasks[0].id
