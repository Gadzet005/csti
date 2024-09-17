class StorageError(Exception):
    pass


class LoadError(StorageError):
    pass


class SaveError(StorageError):
    pass


class FieldError(StorageError):
    def __init__(self, location: tuple[str, ...]):
        self.fieldName = ".".join(location)


class FieldNotFound(FieldError):
    def __str__(self):
        return f"Неизвестное поле: '{self.fieldName}'."


class FieldIsEmpty(FieldError):
    def __str__(self):
        return f"Попытка получения значения из пустого поля: '{self.fieldName}'."
