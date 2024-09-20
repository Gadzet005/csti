class EnvError(Exception):
    pass


class EnvNotInitialized(EnvError):
    def __str__(self):
        return "Директория не инициализирована. Используйте csti init."


class EnvStorageError(EnvError):
    pass
