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
    """Поле не найдено в шаблоне."""

    def __str__(self):
        return f"Неизвестное поле: '{self.fieldName}'."


class FieldIsEmpty(FieldError):
    """Поле присутствует в шаблоне, но не имеет значение."""

    def __str__(self):
        return f"Попытка получения значения из пустого поля: '{self.fieldName}'."


class FieldValueError(FieldError):
    """Поле имеет невалидное значение."""

    def __init__(self, location: tuple[str, ...], value):
        self.fieldName = ".".join(location)
        self.value = value

    def __str__(self):
        return f"Недопустимое значение в поле '{self.fieldName}': {self.value}."
