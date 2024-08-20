from enum import Enum


class TestStatus(Enum):
	ok = "ОК"
	timeLimit = "Превышено максимальное время ожидания"
	memoryLimit = "Превышено максимальное количество памяти"
	wrongAnswer = "Неправильный ответ"
	runtimeError = "Ошибка выполнения"

class TestResult:
	def __init__(self, status: TestStatus, message: str|None = None):
		self._status: TestStatus = status
		self._message: str|None = message

	def __str__(self):
		if not self._message:
			return self._status.value
		return f"{self._status.value}:\n{self._message}"

	@property
	def status(self) -> TestStatus:
		return self._status

	@property
	def message(self) -> str|None:
		return self._message


class TestResultList:
	def __init__(self, results: list[TestResult]|None=None):
		self._results = results if results is not None else []

	def __iter__(self):
		return iter(self._results)

	def __next__(self):
		return next(self._results)
	
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
