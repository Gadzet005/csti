from __future__ import annotations
from typing import override, Any

import os

from csti.consts import APP_NAME
from csti.contest import Contest
from csti.data_storage import DataStorage, StorageTemplate, Group
from csti.data_storage.field import StringField, ListField
from csti.data_storage.exceptions import FieldNotInitialized


class EnvDataStorage(DataStorage):
	FOLDER = "." + APP_NAME
	template = StorageTemplate([
		Group("contest", [
			StringField("id"),
			StringField("selectedTask"),
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
	def _get(self, *location: list[str]) -> Any:
		try:
			with open(self.getPathByLocation(location), "r") as f:
				return f.read()
		except FileNotFoundError:
			raise FieldNotInitialized(location)
	
	@override
	def _set(self, *location: list[str], value):
		path = self.getPathByLocation(location)
		os.makedirs(os.path.dirname(path), exist_ok=True)
		with open(path, "w") as f:
			f.write(str(value))
	
	@property
	def dir(self) -> str:
		return self._dir
	
	def loadContest(self) -> Contest:
		id = self.get("contest", "id")
		tasks = self.get("contest", "tasks")
		selectedTask = self.get("contest", "selectedTask")
		return Contest(id, tasks, selectedTask)
