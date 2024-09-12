class APIException(Exception):
    pass


class AuthException(APIException):
    pass


class ContestException(Exception):
    pass


class TaskException(Exception):
    pass


class ParserError(Exception):
    pass


class CantParseElement(ParserError):
    def __init__(self, element: str):
        self.element = element

    def __str__(self) -> str:
        return f"Не удалочь получить элемент: {self.element}."
