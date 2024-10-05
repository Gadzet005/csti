import typing as t

from csti.storage.config import Config


class TestConfig(Config):
    def __init__(self, data: dict):
        super().__init__("")
        self._data = data

    @t.override
    def save(self):
        pass

    @t.override
    def load(self, force: bool = True):
        pass

    @t.override
    def create(self):
        pass
