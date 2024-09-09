class FieldError(Exception):
    def __init__(self, location: list[str]):
        self.location = location
    
    @property
    def name(self) -> str:
        return '.'.join(self.location)

class FieldNotFound(FieldError):
    def __str__(self):
        return f"Неизвестное поле: '{self.name}'."

class FieldNotInitialized(FieldError):
    def __str__(self):
        return f"Поле '{self.name}' не было инициализировано."
