from functools import cached_property

from csti.contest.contest_interface import ContestInterface
from csti.contest.parser.task_parser import TaskParser
from csti.contest.task.solution import Solution


# TODO: Добавить кэширование и проверку возвращаемого значения в функциях.
class Task:
	def __init__(self, id_: str):
		self._id: str = id_

	@cached_property
	def _task(self) -> bytes:
		return ContestInterface().requestTask(self._id)

	@property
	def id(self) -> str:
		return self._id

	@cached_property
	def info(self) -> dict[str, str]:
		""" Вспомогательная информация """
		return TaskParser.getInfo(self._task)
	
	@property
	def timeLimit(self) -> int:
		""" Ограничение по времени в секундах """
		raw = self.info["Ограничение времени"]
		return int(raw[:-2])
	
	@property
	def memoryLimit(self) -> int:
		""" Ограничение памяти в мегабайтах """
		raw = self.info["Ограничение памяти"]
		return int(raw[:-1])
	
	@property
	def remainingAttemps(self) -> int:
		""" Оставшееся количество попыток """
		return int(self.info["Оставшиеся посылки"])

	@property
	def name(self) -> str:
		""" Название задачи """
		return TaskParser.getName(self._task)

	@property
	def condition(self) -> str:
		""" Условие задачи """
		return TaskParser.getCondition(self._task)

	@property
	def tests(self) -> list[tuple[str, str]]:
		""" Список базовых тестов задачи """
		return TaskParser.getTests(self._task)

	@property
	def solution(self) -> Solution|None:
		""" Последнее отправленное решение """
		return TaskParser.getLastSolution(self._task)

	def sendSolution(self, file: str):
		""" Отправка решения """
		return ContestInterface().sendTask(self._id, file)
