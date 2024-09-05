from __future__ import annotations

import os

from csti.contest_env.data_storage import EnvDataStorage
from csti.contest import Contest
from csti.contest_env.exceptions import ContestEnvException


class ContestEnv:
	""" Управляет папкой для работы с контестом. """

	def __init__(self, dir: str):
		self._dir = dir
		self._storage = EnvDataStorage(dir)
	
	@staticmethod
	def init(dir: str|None = None) -> ContestEnv:
		""" 
		Инициализирует папку для работы с контестом.\n
		@param dir: Директория для инициализации. Если dir = None,
		то инициализирует текущую директорию.
		"""
		
		if dir is None:
			dir = os.getcwd()
		EnvDataStorage.init(envDir=dir)
		return ContestEnv(dir)

	def selectContest(self, contest: Contest):
		""" Смена контеста в рабочей директории. """

		tasks = list(map(lambda x: x.id, contest.tasks))
		self.storage.set("contest", "id", value=contest.id)
		self.storage.set("contest", "tasks", value=tasks)
		self.storage.set("contest", "selectedTask", value=contest.currentTask.id)

		for task in contest.tasks:
			fileName = task.id + contest.lang.fileExtension

			with open(os.path.join(self.dir, fileName), "w") as f:
				f.write(contest.lang.comment + " " + task.name + "\n")
	
	@staticmethod
	def inCurrentDir() -> ContestEnv:
		""" 
		Проверяет, что рабочая (текущая) директория инициализирована
		и возвращает экземплер ContestEnv.
		"""
		env = ContestEnv(os.getcwd())
		if not env.isEnvValid:
			raise ContestEnvException(
				"Рабочая папка не проинциализирована. Используйте csti init."
			)
		return env

	@property
	def dir(self) -> str:
		return self._dir

	@property
	def storage(self) -> EnvDataStorage:
		return self._storage

	@property
	def isEnvValid(self) -> bool:
		""" Инициализирована ли рабочая директория? """
		return os.path.exists(self.storage.dir)
