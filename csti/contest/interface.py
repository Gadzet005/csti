from __future__ import annotations
import abc

from csti.program_view import Program
from csti.contest.exceptions import ContestException


class ContestSystemAPI:
    """ Делает запросы на сервер и обрабатывает результаты. """

    @abc.abstractmethod
    def getContests(self) -> list[Contest]:
        """ Получение всех контестов. """
        pass

    @abc.abstractmethod
    def getContestInfo(self, contestId: Contest.IDType) -> dict:
        """ 
        Информация о контесте:
            "name": str 					Название контеста
            "tasks": list[Task]				Список задач
            "languages": list[Language] 	Список доступных языков
        """
        pass

    @abc.abstractmethod
    def getTaskInfo(self, taskId: Task.IDType) -> dict:
        """ 
        Информация о задаче:
            "id": int								Идентификатор
            "name": str 							Название
            "description": str 						Условие
            "inputFormat": str						Формат входных данных
            "outputFormat": str						Формат выходных данных
            "inputExample": list[tuple[str, str]]   Пример входных и выходных данных
            "timeout": int 							Ограничение по времени в секундах
            "memoryLimit": int						Ограничение по памяти в мегабайтах
            "remainingAttemps": int					Количество оставшихся попыток
            "solutions": list[Solution]				Отправленные решения
            "restrictions": str						Ограничения в задаче
            "isSolved": bool						Решена ли задача?
        """
        pass

    @abc.abstractmethod
    def sendTaskSolution(self, taskId: Task.IDType, solution: Program):
        """ Отправка решения задачи. """
        pass


class Contest(abc.ABC):
    IDType = int

    def __init__(self, contestId: IDType):
        self._id = contestId
        self._manager: ContestSystemAPI|None = None

    @property
    def id(self) -> IDType:
        return self._id
    
    @property
    def manager(self) -> ContestSystemAPI:
        if self._manager is None:
            raise ContestException("RequestManager не найден.")
        return self._manager

class Task:
    IDType = int

    def __init__(self, manager: ContestSystemAPI):
        self._manager = manager
