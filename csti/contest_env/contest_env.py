import os
from typing import Self

from csti.contest import Contest
from csti.contest_env.data_storage import EnvDataStorage
from csti.contest_env.exceptions import ContestEnvException, EnvStorageException
from csti.etc.language import Language


class ContestEnv:
    """ Управляет папкой для работы с контестом. """

    def __init__(self, dir: str):
        self._dir = dir
        self._storage = EnvDataStorage(dir)
    
    @staticmethod
    def init(dir: str|None = None) -> Self:
        """ 
        Инициализирует папку для работы с контестом.\n
        @param dir: Директория для инициализации. Если dir = None,
        то инициализирует текущую директорию.
        """
        
        if dir is None:
            dir = os.getcwd()
        EnvDataStorage.init(envDir=dir)
        return ContestEnv(dir)
    
    def getTaskFilePath(self, taskId: str, lang: Language):
        return os.path.join(self.dir, taskId + lang.defaultfileExtension)

    def clearTaskFiles(self):
        """ Очистка всех файлов с заданиями. """
        try:
            contest = self.storage.loadContest()
            for task in contest.tasks:
                path = self.getTaskFilePath(task.id, contest.lang)
                if os.path.isfile(path):
                    os.remove(path)
        except EnvStorageException:
            pass

    def selectContest(self, contest: Contest):
        """ Смена контеста в рабочей директории. """

        self.clearTaskFiles()

        for task in contest.getTasks():
            path = self.getTaskFilePath(task.id, contest.lang)
            with open(path, "w") as f:
                f.write(contest.lang.comment + " " + task.name + "\n")
        
        self.storage.saveContest(contest)

    @staticmethod
    def inCurrentDir() -> Self:
        """ 
        Проверяет, что рабочая (текущая) директория инициализирована
        и возвращает экземплер ContestEnv.
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
        """ Инициализирована ли рабочая директория? """
        return os.path.exists(self.storage.dir)
