from __future__ import annotations

import os
from typing import Any, override

from csti.etc.settings import APP_NAME
from csti.contest import Contest
from csti.contest_env.exceptions import EnvStorageException
from csti.data_storage import DataStorage, Group, StorageTemplate
from csti.data_storage.exceptions import FieldNotInitialized
from csti.data_storage.field import ListField, StringField


class EnvDataStorage(DataStorage):
	FOLDER = "." + APP_NAME
	template = StorageTemplate([
		Group("contest", [
			StringField("id"),
			StringField("currentTask"),
			ListField("tasks")
		])
	])

	def __init__(self, envDir: str):
		super().__init__()
		self._dir = os.path.join(envDir, self.FOLDER)
	
	@override
	@staticmethod
	def init(envDir: str, *args, **kwargs) -> EnvDataStorage:
		os.makedirs(os.path.join(envDir, EnvDataStorage.FOLDER), exist_ok=True)
		return EnvDataStorage(envDir)

	def getPathByLocation(self, location: list[str]):
		return os.path.join(self._dir, *location)

	@override
	def _get(self, location: list[str]) -> Any:
		try:
			with open(self.getPathByLocation(location), "r") as f:
				return f.read()
		except FileNotFoundError:
			raise FieldNotInitialized(location)
	
	@override
	def _set(self, location: list[str], value):
		path = self.getPathByLocation(location)
		os.makedirs(os.path.dirname(path), exist_ok=True)
		with open(path, "w") as f:
			f.write(str(value))
	
	@property
	def dir(self) -> str:
		return self._dir
	
	def loadContest(self) -> Contest:
		try:
			id = self.get("contest", "id")
			tasks = self.get("contest", "tasks")
			currentTask = self.get("contest", "currentTask")
			return Contest(id, tasks, currentTask)
		except FieldNotInitialized:
			raise EnvStorageException("Контест не выбран.")
	
	def saveContest(self, contest: Contest):
		tasks = list(map(lambda x: x.id, contest.tasks))
		self.set("contest", "id", value=contest.id)
		self.set("contest", "tasks", value=tasks)
		self.set("contest", "currentTask", value=contest.currentTask.id)
