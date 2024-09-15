import abc
from csti.config import Config


class App:
    def __init__(self, name: str, version: str, config: Config):
        self._name = name
        self._version = version
        self._config = config

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def version(self) -> str:
        return self._version
    
    @property
    def config(self) -> Config:
        return self._config
    

class RunableApp(abc.ABC, App):
    @abc.abstractmethod
    def _run(self):
        pass

    def run(self):
        "Запуск приложения."
        self._config.create()
        self._config.load()
        self._run()
