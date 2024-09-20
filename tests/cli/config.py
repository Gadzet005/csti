import typing as t

from csti.data_storage.config import Config


class TestConfig(Config):
    def __init__(self, data: dict):
        super().__init__("")
        self._data = data

    @t.override
    def save(self):
        pass

    @t.override
    def load(self):
        pass

config = TestConfig({
    "contest-system": "ejudje"
})
