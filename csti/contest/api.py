import abc

from csti.etc.language import Language


class ContestSystemAPI(abc.ABC):
    """ Делает запросы на сервер и обрабатывает результаты. """
    
    """ Перечисление языков программирования. """
    Lang = Language

    @abc.abstractmethod
    def getContestInfo(self, contestId: int) -> dict:
        """ 
        Информация о контесте.
        ------------------------------------------------------------
        - name (str):                       Название контеста.
        - tasks (list[Task]):               Список задач.
        - other (dict):                     Специфичная для api информация.
        """
        pass

    @abc.abstractmethod
    def getTaskInfo(self, taskId: int) -> dict:
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
        """
        pass

    @abc.abstractmethod
    def sendTaskSolution(self, taskId: int, code: str, languageId: int):
        """ Отправка решения задачи. """
        pass
