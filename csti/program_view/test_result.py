import typing as t
from enum import Enum


class TestStatus(Enum):
    ok = "ОК"
    timeLimit = "Превышено максимальное время ожидания"
    memoryLimit = "Превышено максимальное количество памяти"
    wrongAnswer = "Неправильный ответ"
    runtimeError = "Ошибка выполнения"


class TestResult:
    def __init__(
        self,
        status: TestStatus,
        input: t.Optional[str] = None,
        output: t.Optional[str] = None,
        expected: t.Optional[str] = None,
        message: t.Optional[str] = None,
    ):
        self._status = status
        self._input = input
        self._output = output
        self._expected = expected
        self._message = message

    @property
    def status(self) -> TestStatus:
        return self._status

    @property
    def input(self) -> t.Optional[str]:
        return self._input

    @property
    def output(self) -> t.Optional[str]:
        return self._output

    @property
    def expected(self) -> t.Optional[str]:
        return self._expected

    @property
    def message(self) -> t.Optional[str]:
        return self._message


class TestResultList:
    def __init__(self, results: t.Optional[t.List[TestResult]] = None):
        self._results = results if results is not None else []

    def __iter__(self):
        return iter(self._results)

    def __getitem__(self, key: int):
        return self._results[key]

    @property
    def total(self) -> int:
        return len(self._results)

    @property
    def passed(self) -> int:
        count = 0
        for result in self._results:
            if result.status == TestStatus.ok:
                count += 1
        return count

    @property
    def arePassedAll(self):
        return self.passed == self.total

    def append(self, *args, **kwargs):
        self._results.append(TestResult(*args, **kwargs))
