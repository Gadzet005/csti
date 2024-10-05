import enum
from csti.contest.exceptions import APIException


class APIError(enum.Enum):
    permissionDenied = "ERR_PERMISSION_DENIED"
    invalidContest = "ERR_INV_CONTEST_ID"
    invalidTask = "ERR_INV_PROB_ID"
    invalidParam = "ERR_INV_PARAM"
    invalidSession = "ERR_INV_SESSION"
    duplicateSubmit = "ERR_DUPLICATE_SUBMIT"


class EjudgeAPIException(APIException):
    def __init__(self, errorCode: str, message: str):
        self.errorCode = errorCode
        self.message = message

    def __str__(self) -> str:
        match (self.errorCode):
            case APIError.invalidContest.value:
                return "Контест с таким id не найден."
            case APIError.permissionDenied.value:
                return "В доступе к контесту отказано. Проверьте логин и пароль."
            case APIError.invalidParam.value:
                return "Выполнение неизвестного действия или неправильные параметры."
            case APIError.invalidSession.value:
                return "Невалидная сессия."
            case APIError.invalidTask.value:
                return "Задача с таким id не найдена."
            case _:
                return f"Неизвестная ошибка '{self.errorCode}': {self.message}."
