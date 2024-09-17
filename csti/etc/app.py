import abc

from csti.config import Config


class App:
    def __init__(self, name: str, config: Config):
        self._name = name
        self._config = config

    @property
    def name(self) -> str:
        return self._name

    @property
    def config(self) -> Config:
        return self._config


class RunableApp(abc.ABC, App):
    @abc.abstractmethod
    def _run(self):
        pass

    def prepare(self):
        "Подготовка приложения к работе."
        self._config.create()
        self._config.load()

    def run(self):
        "Запуск приложения."
        self.prepare()
        self._run()
