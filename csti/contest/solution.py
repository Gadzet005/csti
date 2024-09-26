from dataclasses import dataclass
from enum import Enum


class SolutionStatus(Enum):
    acceptedForReview = "Принято на проверку"
    wrongAnswer = "Неправильный ответ"
    compilationError = "Ошибка компиляции"
    runtimeError = "Ошибка выполнения"
    badOuputFormat = "Неправильный формат вывода"
    unclassifiedError = "Не классифицированная ошибка"
    timeLimit = "Превышено максимальное время работы"


@dataclass
class Solution:
    id: int
    status: SolutionStatus
    testsPassed: int
