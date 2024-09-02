class ContestInterfaceException(Exception):
    pass

class AuthException(ContestInterfaceException):
    pass
 

class ParserError(Exception):
	pass

class CantParseElement(ParserError):
	def __init__(self, element: str):
		self.element = element
	
	def __str__(self) -> str:
		return f"Не удалочь получить элемент задачи: {self.element}."

class ContestException(Exception): pass
