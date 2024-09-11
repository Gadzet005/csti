import abc
from typing import Self

from csti.etc.language import ILanguage, Language


class ContestSystemAPI(abc.ABC):
    """ Делает запросы на сервер и обрабатывает результаты. """
    
    """ Перечисление языков программирования. """
    Lang: ILanguage = Language

    @classmethod
    def getInstance(cls, *args, **kwargs) -> Self:
        """ Создает экземпляр ContestSystemAPI. Предпочтительнее, чем конструктор. """
        return cls(*args, **kwargs)

    @abc.abstractmethod
    def getContestIds(cls) -> list[int]:
        """ Возращает список id контестов. """
        pass

    @abc.abstractmethod
    def getContestInfo(self, contestId: int) -> dict|None:
        """ 
        Информация о контесте.
        ------------------------------------------------------------
        - name (str):                       Название контеста.
        - taskIds (list[int]):              Список id задач.
        - other (dict):                     Специфичная для api информация.

        Если контест с таким id не найден, то возвращается None.
        """
        pass

    @abc.abstractmethod
    def getTaskInfo(self, contestId: int, taskId: int) -> dict|None:
        """ 
        Информация о задаче.
        -------------------------------------------------------------------------------
        - name (str):                               Название.
        - description (str):                        Условие.
        - inputFormat (str):                        Формат входных данных.
        - outputFormat (str):                       Формат выходных данных.
        - inputExample (list[tuple[str, str]]):     Пример входных и выходных данных.
        - timeLimit (int):                          Ограничение по времени в секундах.
        - memoryLimit (int):                        Ограничение по памяти в мегабайтах.
        - remainingAttemps (int):                   Количество оставшихся попыток.

        - solutions (list[dict]):                   Отправленные решения.
            - id (int):                             	Id решения.
            - testPassed (int):                         Количесто пройденых тестов.
            - submissionTime (datetime):            	Время отправки решения.
            - status (str):                         	Статус решения.
            - code (str):                           	Код решения.

        - restrictions (str):                       Ограничения в задаче.
        - isSolved (bool):                          Решена ли задача?
        - other (dict):                             Специфичная для api информация.
        - languageIds (list):                       id языков, доступных в этой задаче.

        Если задание с таким id не найдено, то возвращается None.
        """
        pass

    @abc.abstractmethod
    def sendTaskSolution(
        self, 
        contestId: int, 
        taskId: int, 
        code: str, 
        languageId: int
    ) -> bool:

        """ 
        Отправка решения задачи.
        Возвращает True, если решение успешно отправлено, иначе False.
        """
        pass
